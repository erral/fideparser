fideparser
===========

fideparser is a script to parse `FIDE Ratings website`_ and export the data
of the rated tournaments and their arbiters into another formats (currently
csv, json and an internally pickle-based format)

This scripts relies on `screen-scrapping`_ so if FIDE changes the HTML
the scripts will break :S

I intent to mantain this script, at least once a year to export data of the
previous year, so I will keep an eye on the FIDE site and try to fix the bugs.

Feel free to fork and ask for pull-requests. If you find any issue, use
`the issue tracker in GitHub`_.


Author
========

Mikel Larreategi <larreategi@eibar.org>

FIDE International Arbiter and python developer

.. _`FIDE Ratings website`: http://ratings.fide.com
.. _`screen-scrapping`: https://en.wikipedia.org/wiki/Web_scraping
.. _`the issue tracker in GitHub`: https://github.com/erral/fideparser/issues