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
from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from util import time_to_datetime
from util import duration_to_second
from util import str2id

Base = declarative_base()


def init_db(engine):
    Base.metadata.create_all(engine)


def open_db(options):
    engine = create_engine('sqlite:///' + options.database, echo=options.verbose)
    Session = sessionmaker(engine)
    db = Session()
    init_db(engine)
    return db


def close_db(db):
    if db:
        db.close()


def get_build(db, url):
    build = db.query(Build).filter_by(url=url).first()
    if build:
        build.children = []
    return build


def list_builds(db):
    return db.query(Build).all()


def save_build(db, build):
    db.add(build)
    db.commit()


def update_build(db, build):
    db.merge(build)
    db.commit()


class Build(Base):
    __tablename__ = "build"

    url = Column(String(256), primary_key=True)
    base_url = Column(String(128))
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
    downstream = Column(String(4096))
    upstream = Column(String(256))

    def __init__(self, url, host, name, build_number, start, duration, status, downstream,
                 base_url, trigger, upstream):
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
        self.downstream = ','.join(downstream)
        self.upstream = upstream

    def __repr__(self):
        return '''URL: "%s"\n\tname: %s\n\tbuild #: %s\n\thost: %s\n\tstart: %s\n\tstop: %s
\tduration: %s\n\tstatus: %s\n\tdownstream build: %d\n\tupstream: %s\n''' % (
            self.url, self.name, self.build_number, self.host, self.start, self.stop_t, self.duration, self.status,
            len(self.get_downstream()), self.upstream)

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

    def get_downstream(self):
        if self.downstream:
            return self.downstream.split(',')
        return []
