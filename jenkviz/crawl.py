#!/usr/bin/env python
# -*- coding: utf_8 -*
# (C) Copyright 2012 Nuxeo SAS <http://nuxeo.com>
# Authors: Benoit Delbosc <ben@nuxeo.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
import re
from urlparse import urlparse
from funkload.FunkLoadDocTest import FunkLoadDocTest
from funkload.utils import extract_token
from build import Build


class Crawl(object):
    def __init__(self, db, options):
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
        print "Fetching %d builds" % self.count
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
        self.root.extra = {'start': start,
                           'stop': stop,
                           'duration': duration,
                           'throughput': throughput,
                           'count': self.count}
        return self.root

    def _crawl(self, url):
        parent = self.parse_build(url)
        if self.root is None:
            self.root = parent
        print parent
        if not len(parent.downstream):
            return
        for url in parent.downstream:
            known = False
            if url in self.builds.keys():
                known = True
            build = self.parse_build(url)
            parent.children.append(build)
            if not known:
                self._crawl(url)

    def parse_build(self, url):
        if url in self.builds.keys():
            return self.builds[url]
        self.fl.get(self.server_url + url, description="Get build page " + url)
        self.count += 1
        body = self.fl.getBody()
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
        self.builds[url] = build
        return build
