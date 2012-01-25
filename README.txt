===========
jenkviz
===========

NAME
----

  jenkviz - visualization of a Jenkins build flow using graphviz.

  See this examples of SVG_ output.

  You can see that:

  - Black edge are upstream/downstream dependences
  - Orange edge are only downstream dependences
  - Blue box are for successfull build
  - Yellow box are for unstable build
  - Red box are build in failure

USAGE
-----

  jenkviz [--version] [--logfile=LOGFILE] [--database=DATABASE] COMMAND [OPTIONS] ARGUMENTS


COMMANDS
~~~~~~~~~

  crawl -h

  crawl [--direct] [--output SVG_FILE] JENKINS_BUILD_URL

  Crawl a jenkins URL and produce a SVG graph the build information is
  stored in a local sqlite database.


EXAMPLES
~~~~~~~~~

   jenkviz crawl http://jenkins.site/jenkviz/job_name/42/


INSTALLATION
------------
::

  sudo aptitude install graphviz
  sudo easy_install jenkviz

.. _SVG: http://public.dev.nuxeo.com/~ben/demo.svg
