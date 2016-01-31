#!/usr/bin/python
"""
:mod:`import_events` -- Importing ical events into WordPress posts
==================================================================

.. module:: import_events
   :platform: Unix, Windows
   :synopsis: Importing ical events into WordPress posts.
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

----------------------------------------------------------------------

import_events - is a script which imports ical events into WordPress posts.
Dependent on - pytz, iCalendar and python-wordpress-xmlrpc

<https://python-wordpress-xmlrpc.readthedocs.org/>
<https://github.com/maxcutler/python-wordpress-xmlrpc.git/>
<https://github.com/collective/icalendar/>
pip install pytz

"""
#https://www.python.org/dev/peps/pep-0008/ - coding style
#https://www.python.org/dev/peps/pep-0257/
from lib.ical import export_ics_file, read_ical_file
from lib.wputil import get_wordpress_client, get_all_ids, \
    delete_wp_posts, create_all_posts_from_ical
from lib.util import populate_configs, initiate_logging, loginfo

def main():
    """main function"""

    #Logging
    initiate_logging("import_events.log")
    loginfo('[START IMPORT]')

    #Populate the configs
    parser_config = populate_configs()

    #Config header name
    section = "config"
    ics_url = parser_config.get(section, 'ics_url')
    wp_url = parser_config.get(section, 'wp_url')
    ics_filename = parser_config.get(section, 'ics_filename')
    wp_user = parser_config.get(section, 'wp_user')
    wp_pwd = parser_config.get(section, 'wp_pwd')
    event_category = parser_config.get(section, 'event_category')
    dry_run = parser_config.get(section, 'dry_run')
    
   
    if dry_run.lower() in ['1','true']:
		loginfo('It\'s a DRY run')
		dry_run = True
    else:
        dry_run = False
        
    
    #Export the ICS file
    export_ics_file(ics_url, ics_filename)

    #Initate WordPress Client
    client = get_wordpress_client(wp_url, wp_user, wp_pwd)

    #Getting all IDs to delete
    ids = get_all_ids(client, event_category)

    #Delete wordpress posts
    delete_wp_posts(client, ids, dry_run)

    #Get the new Calendar
    cal = read_ical_file(ics_filename)

    #Create new posts
    create_all_posts_from_ical(client, cal, event_category, dry_run)

    #
    loginfo('[END IMPORT]')

#############
#Execute main
if __name__ == '__main__':
    main()
