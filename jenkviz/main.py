#!/usr/bin/env python
# -*- coding: utf_8 -*
# (C) Copyright 2008-2011 Nuxeo SAS <http://nuxeo.com>
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
"""
Try to do something usefull with a jmeter output.
"""
import os
import sys
from optparse import OptionParser, TitledHelpFormatter
from util import get_version, init_logging
from command import *

DEFAULT_DB = "~/jenkviz.db"
DEFAULT_LOG = "~/jenkviz.log"

USAGE = """jenkviz [--version] [--logfile=LOGFILE] [--database=DATABASE] COMMAND [OPTIONS] [ARGUMENT]

COMMANDS:

  list
     List the imported benchmark in the database.

  info BID
     Give more information about the build flow with the bid number (build identifier).

  crawl [--reverse| URL
     crawl the jenkins. Output the BID number.

  report BID
     Generate the report for the imported build

EXAMPLES

   jenkviz list
      List of crawled build.

   jenkviz import -m"Run 42" http://jenkins/jenkins/job/foo/34/
      Import a build #34 of foo, this will output a BID number.
.
   jenkviz report 1 -o foo.svg
      Build the report of build flow BID 1

"""


def main(argv=sys.argv):
    """Main test"""
    global USAGE
    parser = OptionParser(USAGE, formatter=TitledHelpFormatter(),
                          version="jenkviz %s" % get_version())
    parser.add_option("-v", "--verbose", action="store_true",
                      help="Verbose output")
    parser.add_option("-l", "--logfile", type="string",
                      default=os.path.expanduser(DEFAULT_LOG),
                      help="Log file path")
    parser.add_option("-d", "--database", type="string",
                      default=os.path.expanduser(DEFAULT_DB),
                      help="SQLite db path")
    parser.add_option("-m", "--comment", type="string",
                      help="Add a comment")
    parser.add_option("-r", "--reverse", action="store_true",
                      default=True,
                      help="Reverse crawl")
    parser.add_option("--rmdatabase", action="store_true",
                      default=False,
                      help="Remove existing database")
    parser.add_option("-o", "--output", type="string",
                      help="Report file")

    options, args = parser.parse_args(argv)
    init_logging(options)
    if len(args) == 1:
        parser.error("Missing command")
    cmd = args[1]
    fn = globals()['cmd_' + cmd]
    ret = fn(args[2:], options)
    return ret


if __name__ == '__main__':
    ret = main()
    sys.exit(ret)
