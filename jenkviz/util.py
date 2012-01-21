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

import hashlib
import re
import logging
import pkg_resources
from commands import getstatusoutput
from datetime import datetime
from datetime import timedelta


def graphviz_recurse(parent, out, visited):
    if parent.url in visited:
        return
    visited.append(parent.url)
    out.write('%s [label="%s #%s|%s %s|%s" color=%s URL="%s"]\n' % (
        parent.getId(), parent.name, parent.build_number, parent.start[13:], parent.host, parent.duration,
        parent.color(), parent.full_url()))

    if parent.trigger:
        out.write('%s [color=orange style=filled]\n%s -> %s\n' % (
                parent.trigger, parent.trigger, parent.getId()))
    if not parent.children:
        return
    out.write("%s -> {" % parent.getId())
    for build in parent.children:
        out.write(build.getId() + ";")
    out.write("}\n")
    for build in parent.children:
        graphviz_recurse(build, out, visited)


def graphviz(root, fpath):
    out = open(fpath, "w+")
    out.write("""digraph g {
graph [rankdir=LR];
node [fontsize="16" shape="record"];
info [label="start: %s|stop: %s|duration: %s|number of builds: %s|throughput: %s%%"];
""" % (root.extra['start'], root.extra['stop'], timedelta(seconds=root.extra['duration']), root.extra['count'], root.extra['throughput']))

    visited = []
    graphviz_recurse(root, out, visited)
    out.write("}\n")
    out.close()
    print "Saving " + fpath


def makeSvg(dot_file):
    out_file = dot_file.replace('.dot', '.svg')
    cmd = "dot -Tsvg %s -o %s" % (dot_file, out_file)
    ret, output = getstatusoutput(cmd)
    if ret != 0:
        raise RuntimeError("Failed to run dot cmd: " + cmd +
                           "\n" + str(output))
    print "%s generated." % out_file


def get_version():
    """Retrun the package version."""
    return pkg_resources.get_distribution('jenkviz').version


def init_logging(options):
    if hasattr(logging, '_bb_init'):
        return
    level = logging.INFO
    if options.verbose:
        level = logging.DEBUG
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%m-%d %H:%M:%S',
                        filename=options.logfile,
                        filemode='w')
    console = logging.StreamHandler()
    console.setLevel(level)
    formatter = logging.Formatter('%(message)s')
    console.setFormatter(formatter)
    logging.getLogger('').addHandler(console)
    logging._bb_init = True
    print "Logging to " + options.logfile


def md5sum(filename):
    f = open(filename)
    md5 = hashlib.md5()
    while True:
        data = f.read(8192)
        if not data:
            break
        md5.update(data)
    return md5.hexdigest()


def str2id(filename):
    return re.sub(r"[^a-zA-Z0-9_]", r"_", filename)


# credits goes to Subways and Django folks
class BaseFilter(object):
    """Base filter."""
    def __ror__(self, other):
        return other  # pass-thru

    def __call__(self, other):
        return other | self


class truncate(BaseFilter):
    """Middle truncate string up to length."""
    def __init__(self, length=40, extra='...'):
        self.length = length
        self.extra = extra

    def __ror__(self, other):
        if len(other) > self.length:
            mid_size = (self.length - 3) / 2
            other = other[:mid_size] + self.extra + other[-mid_size:]
        return other


def duration_to_second(duration):
    """Convert jenkins duration into second"""
    match = re.match('^(([0-9])+ h)? ?(([0-9]+) min)? ?(([0-9]+) sec)?$', duration)
    ret = 0
    if match and len(match.groups()) == 6:
        if match.group(2):
            ret += 3600 * int(match.group(2))
        if match.group(4):
            ret += 60 * int(match.group(4))
        if match.group(6):
            ret += int(match.group(6))
    return ret


def time_to_datetime(str_time):
    return datetime.strptime(str_time, '%b %d, %Y %I:%M:%S %p')
