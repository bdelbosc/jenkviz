#!/usr/bin/env python
# (C) Copyright 2011 Nuxeo SAS <http://nuxeo.com>
# Author: bdelbosc@nuxeo.com
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as published
# by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA
# 02111-1307, USA.
#
#
"""jenkviz package setup"""
from setuptools import setup, find_packages
__version__ = '0.1.0'


setup(
    name="jenkviz",
    version=__version__,
    description="Crawl a jenkins build and report stats and graphs about the build flow.",
    long_description=''.join(open('README.txt').readlines()),
    author="Benoit Delbosc",
    author_email="bdelbosc@nuxeo.com",
    url="http://pypi.python.org/pypi/jenkviz",
    download_url="http://pypi.python.org/packages/source/t/jenkviz/jenkviz-%s.tar.gz" % __version__,
    packages=find_packages(),
    license='GPL',
    keywords='jenkins hudson CI chart',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Quality Assurance',
    ],
    # setuptools specific keywords
    install_requires=['funkload', ],
    zip_safe=True,
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'jenkviz = jenkviz.main:main'],
    },
)
