#!/usr/bin/env python
# -*- coding: utf_8 -*
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
   jenkviz.model
   ~~~~~~~~~~~~~~

   This module contains the data models for the Jenkviz.
"""
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2012 Nuxeo SA <http://nuxeo.com>"
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import create_engine
from sqlalchemy.schema import Sequence
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pprint import pformat
from datetime import datetime

DB = '~/jenkviz.db'
Base = declarative_base()
engine = create_engine('sqlite:///' + DB)  # , echo=True)
Session = sessionmaker(engine)
session = Session()


class Build(Base):
    __tablename__ = "build"

    url = Column(String(256), primary_key=True)
    host = Column(String(64))
    name = Column(String(128))
    build_number = Column(Integer)
    start = Column(String(32))
    duration = Column(String(32))
    status = Column(String(32))

    start_t = Column(DateTime)
    stop_t = Column(DateTime)
    duration_s = Column(Integer)
    trigger = Column(String(64))

    def __repr__(self):
        return pformat(self.__dict__)

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
        return "%s_%s" % (self.name.replace('-', '_'), self.build_number)

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

def all_builds():
    return session.query(Build).all()
