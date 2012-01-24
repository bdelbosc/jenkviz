===========
jenkviz
===========

NAME
----

  jenkviz - visualization of a Jenkins build flow using graphviz.

USAGE
-----

  jenkviz [--version] [--logfile=LOGFILE] [--database=DATABASE] COMMAND [OPTIONS] ARGUMENTS


COMMANDS
~~~~~~~~~

  crawl [--direct] [--output SVG_FILE] JENKINS_BUILD_URL

     Crawl a jenkins URL and produce a SVG graph the build information is stored in a local sqlite 
     database.


EXAMPLES
~~~~~~~~~

   jenkviz crawl http://jenkins.site/jenkviz/job_name/42/


INSTALLATION
------------
::
  sudo aptitude install graphviz
  sudo easy_install jenkviz

