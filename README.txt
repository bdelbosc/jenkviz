===========
jenkviz
===========

NAME
----

  jenkviz - visualization of a Jenkins_ build flow using graphviz_.

  See this examples of SVG_ output.

  You can see that:

  - There is summary box that displays:
    - the total elapsed time 
    - the cumulated duration for each build
    - a throughput (duration/elapsed)
  - Black edge are upstream/downstream dependences
  - Orange edge are only downstream dependences
  - Blue box are for successfull build
  - Yellow box are for unstable build
  - Red box are build in failure


USAGE
-----

  jenkviz [--version] [--logfile=LOGFILE] [--database=DATABASE] COMMAND [OPTIONS] ARGUMENTS

  jenkviz -h


COMMANDS
~~~~~~~~~

  crawl [--direct] [--output SVG_FILE] JENKINS_BUILD_URL

  Crawl a Jenkins build for downstream buils and produces a SVG graph
  the build information is stored in a local sqlite database that is
  used as a cache to not request twice a build, it also enable to requests
  data using plain SQL::

    sqlite3 ~/jenkviz.db
    -- Slowest jobs
    sqlite> SELECT name, SUM(duration_s), MAX(duration_s), AVG(duration_s), COUNT(1) 
            FROM build 
	    GROUP BY name
	    ORDER BY SUM(duration_s) DESC 
	    LIMIT 10;
    -- Slave load
    sqlite> SELECT host, SUM(duration_s) FROM build GROUP BY host ORDER BY SUM(duration_s) DESC LIMIT 10;

  The ``--direct`` option shows only downstream/upstream relation,
  removing downstream only link.


EXAMPLES
~~~~~~~~~

   jenkviz crawl http://jenkins.site/jenkviz/job_name/42/

   
LIMITATIONS
~~~~~~~~~~~~

   Due to JENKINS-6211_ bug, this works only for maven job because
   current Jenkins (at least 1.444) don't display build number for
   downstream builds for freestyle jobs or non maven jobs.

   Also sometime downstream build number is None and it stops the
   crawling, in this case Jenkins don't give any way to go directly to
   the downstream builds.

   At the moment Jenkviz don't handle build with multiple upstream
   builds, only taking care of the first one.


INSTALLATION
------------
::

  sudo aptitude install graphviz
  sudo easy_install jenkviz

.. _SVG: http://public.dev.nuxeo.com/~ben/demo.svg
.. _JENKINS-6211: https://issues.jenkins-ci.org/browse/JENKINS-6211
.. _Jenkins: http://jenkins-ci.org/
.. _graphviz: http://www.graphviz.org/
