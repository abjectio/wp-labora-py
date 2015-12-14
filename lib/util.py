"""
:mod:`lib.ical` -- Library for handling ICAL
==================================================================

.. module:: ical
   :platform: Unix, Windows
   :synopsis: Library for handling ical
.. moduleauthor:: Knut Erik Hollund <knut.erik@unlike.no>

This file is part of import_events python code.

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
