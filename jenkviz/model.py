#!/usr/bin/env python
# -*- coding: utf_8 -*
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2012 Nuxeo SA <http://nuxeo.com>"
"""
   jenkviz.model
   ~~~~~~~~~~~~~~

   This module contains the data models for the Jenkviz.
"""
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2012 Nuxeo SA <http://nuxeo.com>"
from datetime import timedelta
from pprint import pformat
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from util import time_to_datetime
from util import duration_to_second


DB = '~/jenkviz.db'
Base = declarative_base()
engine = create_engine('sqlite:///' + DB)  # , echo=True)
Session = sessionmaker(engine)
session = Session()


def open_db(options):
    # TODO: impl
    return None


def close_db(db):
    # TODO: impl
    return


def list_builds(db):
    #return db.query(Build).all()
    return []


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

    def __repr__(self):
        return pformat(self.__dict__)

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
