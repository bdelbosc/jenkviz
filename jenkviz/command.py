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
import logging
from model import open_db, list_builds
from crawl import Crawl
from util import graphviz
from util import makeSvg


def cmd_list(args, options):
    db = open_db(options)
    list_builds(db)
    db.close()
    return 0


def cmd_crawl(args, options):
    if len(args) != 1:
        logging.error("Missing build URL")
        return 1
    db = open_db(options)
    crawl = Crawl(db, options)
    root = crawl.crawl(args[0])
    dot_file = root.getId() + ".dot"
    graphviz(root, dot_file)
    makeSvg(dot_file)
    db.close()
    bid = 3
    if bid:
        logging.info("Build analyzed, build internal identifier (bid): %d" % bid)
    else:
        return 1
    return 0


def cmd_info(args, options):
    if len(args) != 1:
        logging.error('Missing bid')
        return 1
    db = open_db(options)
    bencher = Bencher.getBencherForBid(db, options, args[0])
    print """bid: %(bid)s, from %(start)s to %(end)s, samples: %(count)d, errors: %(error)d""" % bencher.getInfo(args[0])
    db.close()
    return 0


def cmd_report(args, options):
    if len(args) != 1:
        logging.error('Missing bid')
        return 1
    if not options.output:
        logging.error('Missing --output option')
        return 1
    db = open_db(options)
    report = Report(db, options)
    report.buildReport(args[0])
    db.close()
    return 0
