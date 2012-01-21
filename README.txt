===========
jenkviz
===========

NAME
----
jenkviz - visualization of a Jenkins build flow using graphviz.

USAGE
-----

  jenkviz [--version] [--logfile=LOGFILE] [--database=DATABASE] COMMAND [OPTIONS] [ARGUMENT]

COMMANDS
~~~~~~~~~

  list
     List the imported build in the local database

  info BID
     Give more information about build with the bid number (build identifier).

  crawl [--reverse] URL
     Crawl a jenkins URL and import info into a local database. Output the BID number.

  report --output REPORT_FILE
     Generate a SVG report for imported build.

EXAMPLES
~~~~~~~~~

   jenkviz list
      List of imported jenkins builds.

   jenkviz crawl http://localhost/jenkins/job/job-name/42/
      Import a Jenkins build #42 of job-name, this will output a BID number.

   jenkviz report 1 -o /tmp/foo.svg
      Build a SVN chart of build BID 1 into /tmp/foo.svg.


REQUIRES
--------

Jenkviz requires `graphviz <http://www.graphviz.org/>`_, on Debian/Ubuntu::
 
  sudo aptitude install graphviz


INSTALLATION
------------
::

   sudo easy_install jenkviz

