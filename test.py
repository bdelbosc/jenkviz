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
from unittest import TestCase
from jenkviz.util import duration_to_second


class DefaultTestCase(TestCase):

    def test_duration(self):
        self.assertEquals(duration_to_second('1 min'), 60)
        self.assertEquals(duration_to_second('1 min 1 sec'), 61)
        self.assertEquals(duration_to_second('10 min 10 sec'), 610)
        self.assertEquals(duration_to_second('1 sec'), 1)
        self.assertEquals(duration_to_second('55 sec'), 55)
        self.assertEquals(duration_to_second('1 h 1 sec'), 3601)
        self.assertEquals(duration_to_second('1 h 1 min 1 sec'), 3661)
