#!/usr/bin/env python
# -*- coding: utf_8 -*
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2012 Nuxeo SA <http://nuxeo.com>"
"""
   jenkviz.util
   ~~~~~~~~~~~~~~~~

   Misc utils
"""
import hashlib
import re
import logging
import pkg_resources
from datetime import datetime


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


def extract_token(text, tag_start, tag_end):
    """Extract a token from text, using the first occurence of
    tag_start and ending with tag_end. Return None if tags are not
    found."""
    start = text.find(tag_start)
    end = text.find(tag_end, start + len(tag_start))
    if start < 0 or end < 0:
        return None
    return text[start + len(tag_start):end]
