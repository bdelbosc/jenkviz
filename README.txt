===========
jenkviz
===========

NAME
----

  jenkviz - visualization of a Jenkins_ build flow using graphviz_.


DESCRIPTION
-----------

  Tool to crawl a Jenkins site using a build url and producing a SVG_
  output to render the build flow.

  The SVG_ graph displays:
  - A summary box with:

    - the total elapsed time 
    - the cumulated duration for each build
    - a throughput (duration/elapsed)
    - number of builds

  - Black arrows to render upstream and downstream relation
  - Orange arrows to render downstream only relation
  - Build with a blue/yellow/red/gray box for Success/Unstable/Failed/Aborted
    build status

  Build information are stored in a local sqlite database. The
  database is used as a cache to not fetch twice a build page
  but also to get information using plain SQL::

    sqlite3 ~/jenkviz.db
    -- Slowest jobs
    sqlite> SELECT name, SUM(duration_s), MAX(duration_s), AVG(duration_s), COUNT(1)
            FROM build
            GROUP BY name
            ORDER BY SUM(duration_s) DESC
            LIMIT 10;
    -- Slave load
    sqlite> SELECT host, SUM(duration_s) FROM build GROUP BY host ORDER BY SUM(duration_s) DESC LIMIT 10;


USAGE
-----

  jenkviz [--version] [--logfile=LOGFILE] [--database=DATABASE] COMMAND [OPTIONS] ARGUMENTS

  jenkviz -h


COMMANDS
~~~~~~~~~

  crawl [--direct|--reverse|--explore] [--output SVG_FILE] JENKINS_BUILD_URL

  The ``--direct`` option shows only downstream and upstream relation,
  removing downstream only link.

  The ``--reverse`` option crawl backward using upstream builds.

  The ``--explore`` option to keep downstream builds that have
  upstream build out of the scope of the origin build (the upstream
  build is not a descendant of the root build)

EXAMPLES
~~~~~~~~~

  jenkviz crawl http://jenkins.site/jenkviz/job_name/42/

   
LIMITATIONS
-----------

  Jenkviz try to find downstream/upstream build using the web page and
  the REST API to work around the JENKINS-6211_ bug. 


INSTALLATION
------------

  On Debian/Ubuntu::

    sudo aptitude install graphviz
    sudo easy_install jenkviz


SOURCE REPOSITORY
~~~~~~~~~~~~~~~~~~~~

  Jenkviz is currently hosted at github_.


ISSUES AND BUG REPORTS
~~~~~~~~~~~~~~~~~~~~~~~~

  Feature requests and bug reports can be made here:

  * https://github.com/bdelbosc/jenkviz/issues


.. _SVG: http://public.dev.nuxeo.com/~ben/demo.svg
.. _JENKINS-6211: https://issues.jenkins-ci.org/browse/JENKINS-6211
.. _Jenkins: http://jenkins-ci.org/
.. _graphviz: http://www.graphviz.org/
.. _github: https://github.com/bdelbosc/jenkviz
