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
from datetime import timedelta
from util import time_to_datetime
from util import duration_to_second
from util import str2id


class Build(object):
    """ Container for activity information"""
    def __init__(self, url, host, name, build_number, start, duration, status, downstream,
                 base_url, trigger):
        self.url = url
        self.host = host
        self.name = name
        self.build_number = build_number
        self.start = start
        self.duration = duration
        self.status = status
        self.downstream = downstream
        self.children = []
        self.base_url = base_url
        self.trigger = trigger
        self.start_t = time_to_datetime(start)
        self.duration_s = duration_to_second(duration)
        self.stop_t = self.start_t + timedelta(seconds=self.duration_s)

    def getId(self):
        return str2id("%s %s" % (self.name, self.build_number))

    def color(self):
        if self.status == 'Success':
            return "blue"
        if self.status == 'Failure':
            return "red"
        if self.status == 'Unstable':
            return "gold"
        return "black"

    def full_url(self):
        return self.base_url + self.url

    def __repr__(self):
        return 'URL: "%s"\n\tname: %s\n\tbuild #: %s\n\thost: %s\n\tstart: %s\n\tstop: %s\n\tduration: %s\n\tstatus: %s\n\tdownstream build: %d\n' % (
            self.url, self.name, self.build_number, self.host, self.start, self.stop_t, self.duration, self.status,
            len(self.downstream))
