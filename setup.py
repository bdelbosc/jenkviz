#!/usr/bin/env python
__author__ = "Benoit Delbosc"
__copyright__ = "Copyright (C) 2012 Nuxeo SA <http://nuxeo.com/>"
__version__ = '0.1.1'
"""jenkviz package setup"""
from setuptools import setup, find_packages


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
    install_requires=['requests', 'sqlalchemy'],
    zip_safe=True,
    test_suite='nose.collector',
    entry_points={
        'console_scripts': [
            'jenkviz = jenkviz.main:main'],
    },
)
