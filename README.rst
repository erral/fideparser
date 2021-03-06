fideparser
===========

.. image:: https://img.shields.io/pypi/v/fideparser.svg
        :target: https://pypi.python.org/pypi/fideparser

.. image:: https://travis-ci.com/erral/fideparser.svg?branch=master
        :target: https://travis-ci.com/erral/fideparser

.. image:: https://coveralls.io/repos/github/erral/fideparser/badge.svg?branch=master
        :target: https://coveralls.io/github/erral/fideparser?branch=master

.. image:: https://img.shields.io/pypi/pyversions/fideparser.svg
        :alt: PyPI - Python Version



fideparser is a script to parse `FIDE Ratings website`_ and export the data
of the rated tournaments.

FIDE (*Federation International des Echecs* or *World Chess Federation*) is the
internationally recognised governing body of chess. Every month a lot of
tournaments are played all over the world and many of them are rated for
the FIDE Rating List which is published on 1st day of each month.

FIDE publishes all the rating reports of those rated chess tournaments online at
http://ratings.fide.com but they don't provide any API or automatized way
of exporting or getting that information.

So this script allows you to export all the data of those tournaments (based
on country and rating period) to CSV, JSON and an internal pickle-based format.
This script doesn't export the player data from each tournament, but the
metadata about the tournament: name, start- and end-dates, format, player number,
arbiter and organizer name, ...

This scripts relies on `screen-scrapping`_ so if FIDE changes the HTML
the script will break :S

I intend to mantain this script at least once a year to export data of the
previous year, so I will keep an eye on the FIDE site and try to fix the bugs.

Feel free to fork and ask for pull-requests. If you find any issue, use
`the issue tracker in GitHub`_.

Dependencies
==============

This script depends on BeautifulSoup4_ an excelent HTML parser used, among other
things, for doing screen-scrapping tasks. The scripts pulls the correct version
of BeautifulSoup4_ so there's no need to do anything on your side to install it.


Installation
===================

Install using pip::

  $ pip install fideparser


And to upgrade to a newer version, just use pip again::

  $ pip install --upgrade fideparser


Use
======

All options are explained in the help, that you can get running this::

  $ export_fide_tournaments -h

Examples
==========

Export all data from spanish tournaments rated on January 2013 in csv format::

  $ export_fide_tournaments ESP 2013-01-01 2013-january-spain.csv csv

Export all data from french tournaments rated on July 2013 in binary format::

  $ export_fide_tournaments FRA 2012-07-01 2012-july.binary binary

Use the previously exported binary file from France, to create a JSON file::

  $ export_fide_tournaments FRA 2012-07-01 2012-july.json json --datafile 2012-july.binary

Use the previously exported binary file from France, to create a csv file::

  $ export_fide_tournaments FRA 2012-07-01 2012-july.csv csv --datafile 2012-july.binary

If you want to export more arbiter data, append the optional flag `--arbiter-data`::

  $ export_fide_tournaments ESP 2013-01-01 2013-january-spain.csv csv --arbiter-data

If you want to export the report data (currently only the number of players present
in the tournament report), append the optional flag `--report-data`::

  $ export_fide_tournaments ESP 2013-01-01 2013-january-spain.csv csv --report-data

A script for merging CSV files is also provided, usefull to merge files generated
by export_fide_tournaments script. It can be used as follows::

  $ merge_csv_files outfile.csv 2013-january-spain.csv 2012-july.csv

Author
========

Mikel Larreategi <larreategi@eibar.org>

FIDE International Arbiter and python developer

.. _`FIDE Ratings website`: http://ratings.fide.com
.. _`screen-scrapping`: https://en.wikipedia.org/wiki/Web_scraping
.. _`the issue tracker in GitHub`: https://github.com/erral/fideparser/issues
.. _virtualenv: http://pypi.python.org/pypi/virtualenv
.. _BeautifulSoup4: http://www.crummy.com/software/BeautifulSoup/
