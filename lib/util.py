"""
:mod:`lib.util` -- Utility library
==================================================================

.. module:: util
   :platform: Unix, Windows
   :synopsis: Library for handling ical
.. moduleauthor:: Knut Erik Hollund <knut.erik@unlike.no>

This file is part of import_events python code.

import_events is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

import_events is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with import_events.  If not, see <http://www.gnu.org/licenses/>.

"""
import sys
import logging
import ConfigParser

def initiate_logging(file_name):
    """ Initate a logger with configs """
    logging.basicConfig(filename=file_name, level=logging.INFO)

def logerror(error_message):
    """Logging error message"""
    logging.error(error_message)

def logdebug(debug_message):
    """Logging error message"""
    logging.debug(debug_message)

def loginfo(info_message):
    """Logging info message"""
    logging.info(info_message)

def populate_configs():
    """Populating all configs from a config file."""
    #Get config file to read
    if len(sys.argv) <= 1:
        logerror('You need to pass a parameter with a config file !')
        logerror('[EXIT AND ENDS IMPORT]')
        sys.exit(2)

    config_filename = sys.argv[1]
    parser = ConfigParser.ConfigParser()
    try:
        parser.readfp(open(config_filename))
        loginfo('Reading configs from file : [' + config_filename + ']')
    except IOError as exception:
        logerror(('Could not read configfile !! - %s ', exception))
        logerror('[EXIT AND ENDS IMPORT]')
        sys.exit(2)

    return parser
