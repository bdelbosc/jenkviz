#!/usr/bin/env python
# -*- coding: utf_8 -*
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2012 Nuxeo SA <http://nuxeo.com>"
"""
   jenkviz.crawl
   ~~~~~~~~~~~~~~~~

   Crawl a Jenkins to extract builds flow.
"""
import sys
import os
import re
import logging
from requests import get as http_get
from model import Build
from util import str2id
from util import extract_token
from util import split_jenkins_url
from model import get_build
from model import save_build
from model import update_build


class Crawl(object):
    def __init__(self, db, options):
        self.db = db
        self.options = options
        self.builds = {}
        self.count = 0
        self.root = None
        if options.verbose:
            self.req_config = {'verbose': sys.stderr}
        else:
            self.req_config = {'verbose': None}

    def crawl(self, url):
        self.url = url
        path = split_jenkins_url(url)
        self.server_url = path[0]
        self.base_path = path[2]
        self.path_root = path[1]
        self._crawl(self.path_root)
        self.clean(self.root)
        self.root.extra = self.stats()
        return [self.root]

    def _crawl(self, url):
        parent = self.get_build(url)
        if self.root is None:
            self.root = parent
        print parent
        if not len(parent.get_downstream()):
            return
        for child_url in parent.get_downstream():
            known = False
            if child_url in self.builds.keys():
                known = True
            child = self.get_build(child_url)
            if not self.options.direct or parent.url in child.get_upstream():
                parent.children.append(child)
            if not known:
                self._crawl(child_url)

    def reverse_crawl(self, url):
        self.url = url
        ret = split_jenkins_url(url)
        self.server_url = ret[0]
        self.path_leaf = ret[1]
        self.roots = []
        self._reverse_crawl(self.path_leaf)
        # TODO: disable cache and craw from roots
        # for root in self.roots:
        #    self._crawl(root.url)
        self.roots[0].extra = self.stats()
        return self.roots

    def _reverse_crawl(self, url):
        child = self.get_build(url)
        print child
        if len(child.get_upstream()) == 0:
            self.roots.append(child)
            return
        for parent_url in child.get_upstream():
            known = False
            if parent_url in self.builds.keys():
                known = True
            parent = self.get_build(parent_url)
            parent.children.append(child)
            if not known:
                self._reverse_crawl(parent_url)

    def get_build(self, url):
        self.count += 1
        # 1. fetch from cache
        if url in self.builds.keys():
            return self.builds[url]
        ret = None
        # 2. fetch from local db
        ret = self.fetch_build_from_db(url)
        # 3. fetch jenkins page
        if ret is None or self.options.update:
            build = self.fetch_build(url)
            if build is None:
                return None
            # 3.1 persist build
            if ret is None:
                self.save_build_to_db(build)
            else:
                self.update_build_to_db(build)
            ret = build
        # 4. update cache
        self.builds[url] = ret
        return ret

    def fetch_build(self, url):
        if self.options.from_file:
            body = self.fetch_build_from_file(url)
        else:
            body = self.fetch_from_server(url)
        ret = self.parse_build(url, body)
        children = self.get_rest_children(ret)
        for child in ret.get_downstream():
            if child not in children:
                children.append(child)
        ret.set_downstream(children)
        if ret and self.options.to_file:
            self.save_build_to_file(ret, body)
        return ret

    def fetch_build_from_db(self, url):
        return get_build(self.db, url)

    def save_build_to_db(self, build):
        save_build(self.db, build)

    def update_build_to_db(self, build):
        update_build(self.db, build)

    def fetch_from_server(self, url, params=None, ok_codes=None):
        response = http_get(self.server_url + url, data=params, config=self.req_config)
        if ok_codes is None:
            ok_codes = [200, ]
        if response.status_code not in ok_codes:
            logging.error('Failure: %s%s return %s' % (self.server_url, url, response.status_code))
            return "ERROR: %s: %s" % (response.status_code, response.text)
        return response.text

    def fetch_build_from_file(self, url):
        dir_path = self.options.from_file
        build_id = str2id(' '.join([i for i in url.split('/') if i][-2:]))
        file_path = os.path.join(dir_path, build_id + '.txt')
        body = '\n'.join(open(file_path).readlines())
        return body

    def save_build_to_file(self, build, body):
        dir_path = self.options.to_file
        build_id = build.getId()
        file_path = os.path.join(dir_path, build_id + '.txt')
        open(file_path, 'w+').write(body.encode('utf-8'))

    def get_rest_children(self, build):
        """Use the REST API to discover children build."""
        job_url = self.base_path + "/" + build.name
        job_api_url = job_url + '/api/xml?xpath=//downstreamProject/name/text()'
        jname_pattern = re.compile('^[0-9a-zA-Z\-\_]+$')
        jbuild_pattern = re.compile('^[0-9]+$')
        # 1. query the job page to get a list of downstream jobs
        body = self.fetch_from_server(job_api_url, ok_codes=[200, 404, 500])
        children_names = []
        match = re.findall(r'matched ([0-9]*) ', body)
        if len(match):
            for i in range(1, int(match[0]) + 1):
                body = self.fetch_from_server(job_url + '/api/xml?xpath=//downstreamProject[%d]/name/text()' % i,
                                              ok_codes=[200, 404])
                if jname_pattern.match(body.strip()):
                    children_names.append(str(body))
                    # print "  Downstream job: %s" % body
        elif jname_pattern.match(body.strip()):
            children_names.append(str(body))
        ret = []
        # 2. for each downstream ask a matching upstream build
        for child in children_names:
            url = self.base_path + "/" + child
            url += '/api/xml?depth=1&xpath=//build[action/cause/upstreamProject="%s"%%20and%%20action/cause/upstreamBuild=%s]/number/text()' % (build.name, build.build_number)
            body = self.fetch_from_server(url, ok_codes=[200, 404])
            if jbuild_pattern.match(body.strip()):
                ret.append(self.base_path + "/" + str(child) + "/" + str(body) + "/")
                # print " Found downstream build: %s %s" % (child, body)
        return ret

    def parse_build(self, url, body):
        if body.startswith('ERROR'):
            ret = split_jenkins_url(url)
            name = ret[3]
            build_number = ret[4]
            return Build(url, body, name, build_number, None, None, 'Unknown', [],
                         self.server_url, '', [])
        name = extract_token(body, '<title>', ' ')
        h1 = extract_token(body, '<h1>', '</h1>')
        status = extract_token(h1, 'alt="', '"')
        build_number = extract_token(h1, 'Build #', '\n')
        start = extract_token(h1, "(", ")")
        duration = extract_token(body, '/buildTimeTrend">', '</a')
        host = extract_token(body, '<a href="/jenkins/computer/', '"')
        downstream_builds = extract_token(body, 'h2>Downstream Builds</h2', '</ul>')
        trigger = "Unknown"
        upstream_urls = []
        if 'Started by upstream project' in body:
            upstream = extract_token(body, 'Started by upstream project', '</td')
            upstream_urls = re.findall(r'href="([^"]+[0-9]/)"', upstream)
            trigger = None
        if 'Started by GitHub push' in body:
            try:
                trigger = "commit_" + extract_token(body, 'commit: ', '<')
            except TypeError:
                trigger = "commit_unknown"
        if 'Started by user' in body:
            trigger = "started_by_user"
        downstream_urls = []
        if downstream_builds:
            downstream_urls = re.findall(r'href="([^"]+[0-9]/)"', downstream_builds)
        build = Build(url, host, name, build_number, start, duration, status, downstream_urls,
                      self.server_url, trigger, upstream_urls)
        return build

    def stats(self):
        """Compute statistics about the build tree."""
        start = stop = None
        duration = 0
        for build in self.builds.itervalues():
            if not build.start_t or not build.stop_t:
                continue
            if start is None or build.start_t < start:
                start = build.start_t
            if stop is None or build.stop_t > stop:
                stop = build.stop_t
            duration += build.duration_s
        elapsed = stop - start
        throughput = 0
        if elapsed.seconds:
            throughput = duration * 100. / elapsed.seconds
        ret = {'start': start,
               'stop': stop,
               'elapsed': elapsed,
               'duration': duration,
               'throughput': throughput,
               'count': len(self.builds)}
        return ret

    def clean_orphan(self, parent):
        """Remove build with no direct upstream."""
        for child in parent.children:
            if len(set(child.get_upstream()).intersection(set(self.builds.keys()))) == 0:
                parent.children.remove(child)
                if child.url in self.builds:
                    print "Removing orphean: %s" % child.url
                    self.builds.pop(child.url)
            self.clean_orphan(child)

    def list_builds(self, parent, builds):
        """Walk the tree to list the builds."""
        if parent.url not in builds:
            builds.append(parent.url)
        for build in parent.children:
            self.list_builds(build, builds)

    def clean(self, parent):
        if not self.options.explore:
            for i in range(10):
                # wtf is that :)
                self.clean_orphan(parent)
        all_builds = []
        self.list_builds(parent, all_builds)
        for url in self.builds.keys():
            if url not in all_builds:
                self.builds.pop(url)
