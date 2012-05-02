=================
jenkviz CHANGES
=================

.. contents:: Table of Contents


jenkviz git master
--------------------

:git: https://github.com/bdelbosc/jenkviz

:Target: 0.3.2


jenkviz 0.3.1
------------------

:Package: http://pypi.python.org/packages/source/j/jenkviz/jenkviz-0.3.1.tar.gz

:github: https://github.com/bdelbosc/jenkviz/tree/0.3.1

:Released date: 2012-05-02

Bug Fixes
~~~~~~~~~~

* Fix broken ``--reverse`` option.

jenkviz 0.3.0
------------------

:Package: http://pypi.python.org/packages/source/j/jenkviz/jenkviz-0.3.0.tar.gz

:github: https://github.com/bdelbosc/jenkviz/tree/0.3.0

:Released date: 2012-01-31

Upgrade notes
~~~~~~~~~~~~~~

* You should use the ``--update`` options or remove your existing
  database ``~/jenkviz.db``.


New Features
~~~~~~~~~~~~~

* Use the Jenkins REST API to discover downstream builds, this
  make it work with free style job.
 

Bug Fixes
~~~~~~~~~~

* Fix duration parsing for hour.

* Fix duration parsing for second in float format.


jenkviz 0.2.0
------------------

:Package: http://pypi.python.org/packages/source/j/jenkviz/jenkviz-0.2.0.tar.gz

:github: https://github.com/bdelbosc/jenkviz/tree/0.2.0

:Released date: 2012-01-26


New Features
~~~~~~~~~~~~~~

* Adding ``--explore`` options

* Adding ``--reverse`` to crawl backward

Bug Fixes
~~~~~~~~~~

* Handles multiple upstream build.

* Handles 404 on deleted build.

* Fix color for Failed and Aborted build.


jenkviz 0.1.1
------------------

:Package: http://pypi.python.org/packages/source/j/jenkviz/jenkviz-0.1.1.tar.gz

:github: https://github.com/bdelbosc/jenkviz/tree/0.1.1

:Released date: 2012-01-25

First release.




