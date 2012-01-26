#!/usr/bin/env python
# -*- coding: utf_8 -*
"""
Try to do something usefull with a jmeter output.
"""
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2012 Nuxeo SA <http://nuxeo.com>"
import os
import sys
from optparse import OptionParser, TitledHelpFormatter
from util import get_version, init_logging
from command import *

DEFAULT_DB = "~/jenkviz.db"
DEFAULT_LOG = "~/jenkviz.log"

USAGE = """jenkviz [--version] [--logfile=LOGFILE] [--database=DATABASE] COMMAND [OPTIONS] [ARGUMENT]

COMMANDS:

  crawl [OPTIONS] URL
     crawl the jenkins build produces a SVG file.

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
    parser.add_option("-o", "--output", type="string",
                      help="SVG output file")
    parser.add_option("--from-file", type="string",
                      help="Use html files in the the FROM_FILE directory instead of querying jenkins server.")
    parser.add_option("--to-file", type="string",
                      help="Save jenkins page into the TO_FILE directory.")
    parser.add_option("-r", "--reverse", action="store_true",
                      default=False,
                      help="Reverse crawl")
    parser.add_option("--direct", action="store_true",
                      default=False,
                      help="Display only direct upstream dependencies")
    parser.add_option("--explore", action="store_true",
                      default=False,
                      help="Display downstream build with external upstream")
    parser.add_option("-u", "--update", action="store_true",
                      default=False,
                      help="Always fetch build from server (update local database)")

    options, args = parser.parse_args(argv)
    if options.explore:
        options.direct = False
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
