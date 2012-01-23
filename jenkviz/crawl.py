#!/usr/bin/env python
# -*- coding: utf_8 -*
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2012 Nuxeo SA <http://nuxeo.com>"
"""
   jenkviz.crawl
   ~~~~~~~~~~~~~~~~

   Crawl a Jenkins to extract builds flow.
"""
import os
import re
from urlparse import urlparse
from funkload.FunkLoadDocTest import FunkLoadDocTest
from funkload.utils import extract_token
from build import Build
from util import str2id


class Crawl(object):
    def __init__(self, db, options):
        self.db = db
        self.options = options
        self.fl = FunkLoadDocTest(debug=False)
        self.fl._simple_fetch = True
        self.builds = {}
        self.count = 0
        self.root = None

    def crawl(self, url):
        self.url = url
        u = urlparse(url)
        self.path_root = u.path
        self.server_url = url[:-len(self.path_root)]
        self._crawl(self.path_root)
        self.root.extra = self.stats()
        return self.root

    def _crawl(self, url):
        parent = self.get_build(url)
        if self.root is None:
            self.root = parent
        print parent
        if not len(parent.downstream):
            return
        for url in parent.downstream:
            known = False
            if url in self.builds.keys():
                known = True
            build = self.get_build(url)
            parent.children.append(build)
            if not known:
                self._crawl(url)

    def get_build(self, url):
        self.count += 1
        # 1. fetch from cache
        if url in self.builds.keys():
            return self.builds[url]
        ret = None
        # 2. fetch from local db
        ret = self.fetch_build_from_db(url)
        # 3. fetch jenkins page
        if ret is None:
            ret = self.fetch_build(url)
            # 3.1 persist build
            self.save_build_to_db(ret)
        # 4. update cache
        self.builds[url] = ret
        return ret

    def fetch_build(self, url):
        if self.options.from_file:
            return self.fetch_build_from_file(url)
        return self.fetch_build_from_server(url)

    def fetch_build_from_db(self, url):
        # TODO: impl
        return None

    def save_build_to_db(self, build):
        # TODO: impl
        pass

    def fetch_build_from_server(self, url):
        self.fl.get(self.server_url + url, description="Get build page " + url)
        ret = self.parse_build(url, self.fl.getBody())
        if self.options.to_file:
            self.save_build_to_file(ret, self.fl.getBody())
        return ret

    def fetch_build_from_file(self, url):
        dir_path = self.options.from_file
        build_id = str2id(' '.join([i for i in url.split('/') if i][-2:]))
        file_path = os.path.join(dir_path, build_id + '.txt')
        body = '\n'.join(open(file_path).readlines())
        return self.parse_build(url, body)

    def save_build_to_file(self, build, body):
        dir_path = self.options.to_file
        build_id = build.getId()
        file_path = os.path.join(dir_path, build_id + '.txt')
        open(file_path, 'w+').write(body)

    def parse_build(self, url, body):
        name = extract_token(body, '<title>', ' ')
        h1 = extract_token(body, '<h1>', '</h1>')
        status = extract_token(h1, 'alt="', '"')
        build_number = extract_token(h1, 'Build #', '\n')
        start = extract_token(h1, "(", ")")
        duration = extract_token(body, '/buildTimeTrend">', '</a')
        host = extract_token(body, '<a href="/jenkins/computer/', '"')
        downstream_builds = extract_token(body, 'h2>Downstream Builds</h2', '</ul>')
        trigger = "Unknown"
        if 'Started by upstream project' in body:
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
                      self.server_url, trigger)
        return build

    def stats(self):
        """Compute statistics about the build tree."""
        start = stop = None
        duration = 0
        for build in self.builds.itervalues():
            if start is None or build.start_t < start:
                start = build.start_t
            if stop is None or build.stop_t > stop:
                stop = build.stop_t
            duration += build.duration_s
        duration_total = stop - start
        throughput = 0
        if duration_total.seconds:
            throughput = duration * 100. / duration_total.seconds
        ret = {'start': start,
               'stop': stop,
               'duration': duration,
               'throughput': throughput,
               'count': self.count}
        return ret
