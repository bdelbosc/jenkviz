#!/usr/bin/env python
# -*- coding: utf_8 -*
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2012 Nuxeo SA <http://nuxeo.com>"
"""
   jenkviz.graphviz
   ~~~~~~~~~~~~~~~~

   Generate a graphviz dot file and svg files from a build tree.
"""
from commands import getstatusoutput
from datetime import timedelta


def graphviz(root, svg_file):
    """Create a fpath svg from build tree."""
    dot_file = svg_file.replace('.svg', '.dot')
    out = open(dot_file, "w+")
    out.write("""digraph g {
graph [rankdir=LR];
node [fontsize="16" shape="record"];
info [label="start: %s|stop: %s|elapsed: %s|duration: %s|number of builds: %s|throughput: %s%%"];
""" % (root.extra['start'], root.extra['stop'], root.extra['elapsed'], timedelta(seconds=root.extra['duration']),
       root.extra['count'], root.extra['throughput']))

    visited = []
    _graphviz_recurse(root, out, visited)
    out.write("}\n")
    out.close()
    _make_svg(dot_file, svg_file)


def _graphviz_recurse(parent, out, visited):
    if parent.url in visited:
        return
    visited.append(parent.url)
    out.write('%s [label="%s #%s|%s %s|%s" color=%s URL="%s"]\n' % (
        parent.getId(), parent.name, parent.build_number, str(parent.start_t)[11:], parent.host, parent.duration,
        parent.color(), parent.full_url()))

    if parent.trigger:
        out.write('%s [color=orange style=filled]\n%s -> %s\n' % (
                parent.trigger, parent.trigger, parent.getId()))
    if not parent.children:
        return
    out.write("%s -> {" % parent.getId())
    for build in parent.children:
        if build.upstream == parent.url:
            out.write(build.getId() + ";")
    out.write("}\n")
    for build in parent.children:
        if build.upstream != parent.url:
            out.write('%s -> %s [color=orange]\n' % (parent.getId(), build.getId()))
    for build in parent.children:
        _graphviz_recurse(build, out, visited)


def _make_svg(dot_file, svg_file):
    cmd = "dot -Tsvg %s -o %s" % (dot_file, svg_file)
    ret, output = getstatusoutput(cmd)
    if ret != 0:
        raise RuntimeError("Failed to run dot cmd: " + cmd +
                           "\n" + str(output))
