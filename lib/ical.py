"""
:mod:`lib.ical` -- Library for handling ICAL
==================================================================

.. module:: ical
   :platform: Unix, Windows
   :synopsis: Library for handling ical
.. moduleauthor:: Knut Erik Hollund <knut.erik@unlike.no>

This file is part of import_events python code.

"""

from icalendar import Calendar
from subprocess import check_output
from lib.util import loginfo, logerror
import sys

def export_ics_file(ics_url, output_file):
    """Read configurations from file.

    :param ics_url: URL to ICS stream/ICal file
    :param output_file: Name of file to write the ICal resluts
    :return: returns nothing
    """

    #EXPORT ICS
    loginfo('Get ICS file: [' + ics_url + ']')

    try:
        export_ics = check_output(["curl", "--silent", ics_url])
        if export_ics:
            ofile = open(output_file, 'w')
            ofile.write(export_ics)
            ofile.close()
    except IOError as exception:
        logerror(('Could not get ICS File !! - %s ', exception))
        logerror('[EXIT AND ENDS IMPORT]')
        sys.exit(2)


def read_ical_file(filename):
    """Read the ICAL file"""

    #OPEN ICS FILE
    loginfo('Reading ICAL file: [' + filename +']')
    try:
        cal = Calendar.from_ical(open(filename, 'rb').read())
        return cal
    except IOError as exception:
        logerror(('Could not get an Calendar from file !! \
         - %s - FILE: %s ', exception, filename))
        logerror('[EXIT AND ENDS IMPORT]')
        sys.exit(2)
