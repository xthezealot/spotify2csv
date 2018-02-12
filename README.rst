Spotify2CSV
===========

Convert Spotify URLs to tracks info in CSV format.

Install
-------

.. code:: sh

    pip3 install spotify2csv

Usage
-----

::

    usage: spotify2csv [-h] [-u] urls_file tracks_file

    Convert Spotify URLs to tracks info in CSV format.

    positional arguments:
      urls_file     the Spotify URLs list file (one URL per line)
      tracks_file   the filename for saving the tracks info as CSV

    optional arguments:
      -h, --help    show this help message and exit
      -u, --update  also update info from tracks file (if it already exists and
                    contains tracks
