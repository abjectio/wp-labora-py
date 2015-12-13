#!/usr/bin/python
"""
:mod:`import_events` -- Importing ical events into WordPress posts
==================================================================

.. module:: import_events
   :platform: Unix, Windows
   :synopsis: Importing ical events into WordPress posts.
.. moduleauthor:: Eric Cleese <knut.erik@unlike.no>

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
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, DeletePost
from wordpress_xmlrpc.methods.users import GetUserInfo
from datetime import datetime
from icalendar import Calendar, vDDDTypes, Event
from subprocess import check_output
import ConfigParser
import os
import sys
import logging


def populate_configs():
	"""Populating all configs from a config file."""

	#Get config file to read
	if len(sys.argv)<=1:
		logging.error('You need to pass a parameter with a config file !')
		logging.error('[EXIT AND ENDS IMPORT]')
		sys.exit(2)

	cfgfilename = sys.argv[1]
	parser = ConfigParser.ConfigParser();
	try:		
		parser.readfp(open(cfgfilename))
		logging.info('Reading configs from file : [' + cfgfilename + ']')
	except Exception as e:
		logging.error('Could not read configfile !! - %s ', e)
		logging.error('[EXIT AND ENDS IMPORT]')
		sys.exit(2)
	return parser


def export_ics_file(ics_url, output_file):
	"""Read configurations from file.
	
	:param ics_url: URL to ICS stream/ICal file
	:param output_file: Name of file to write the ICal resluts	
	:return: returns nothing
	"""
	
	#EXPORT ICS
	logging.info('Get ICS file: [' + ics_url + ']')
	
	try:
		export_ics = check_output(["curl","--silent",ics_url])
		if export_ics:
			f = open(output_file,'w')
			f.write(export_ics)
			f.close()
	except Exception as e:
		logging.error('Could not get ICS File !! - %s ', e)
		logging.error('[EXIT AND ENDS IMPORT]')
		sys.exit(2)



def get_wordpress_client(wp_url, wp_user, wp_pwd):
	"""Initate a WordPress connection - xmlrpc."""
	
	#New WordPress object
	logging.info('Initate WordPress client Instance')
	
	try:
		wp = Client(wp_url + '/xmlrpc.php', wp_user, wp_pwd)
		return wp
	except Exception as e:
		logging.error('Could not get wordpress client !! - %s - URL: %s ', e, wp_url)
		logging.error('[EXIT AND ENDS IMPORT]')
		sys.exit(2)		


def get_all_ids(client, event_category):
	"""Get all WordPressPost IDs of a specific type"""

	#Get all IDs of Posts of post_type 'event'
	logging.info('Get all posts with category-event: [' + event_category + '] and delete those')
	offset = 0
	increment = 10
	ids = []
	while True:
		posts = client.call(GetPosts({'post_type': 'event', 'number': increment, 'offset': offset}))
		if len(posts) == 0:
			break #no more posts
		for one_post in posts:
			if (one_post.terms[0].name == event_category):
				ids.append(one_post.id)
		offset += increment
	#Return array of WordPress post IDs
	return ids
	

def delete_wp_posts(client, ids, dry_run):
	"""Delete a range of WordPress posts"""

	#Iterate and delete posts
	for delete_id in ids:
		logging.info('Deleting WordpressPost with ID: [' + delete_id + ']')	
		if not dry_run:
			client.call(DeletePost(delete_id))
				
	logging.info('Deleted %s WordPress posts',len(ids))


def read_ical_file(filename):
	"""Read the ICAL file"""	

	#OPEN ICS FILE
	logging.info('Reading ICAL file: [' + filename +']')	
	try:
		cal = Calendar.from_ical(open(filename,'rb').read())
		return cal
	except Exception as e:
		logging.error('Could not get an Calendar from file !! - %s - FILE: %s ', e, filename)
		logging.error('[EXIT AND ENDS IMPORT]')
		sys.exit(2)


def create_new_wp_post(client, component, event_category, dry_run):
	"""Create a new WordPress post"""
	
	summary = component.get('SUMMARY').encode('UTF-8','backslashreplace')
	start_event = component.get('DTSTART').dt.strftime('%Y-%m-%d %H:%M')
	end_event = component.get('DTEND').dt.strftime('%Y-%m-%d %H:%M')	
	end_frequency_event = component.get('DTEND').dt.strftime('%Y-%m-%d')	
	event_description = component.get('DESCRIPTION').encode('UTF-8','backslashreplace')
	#LOCATION event_location = component.get('LOCATION').encode('UTF-8','backslashreplace')

	# Create a new post
	new_post = WordPressPost()
	new_post.title = summary
	new_post.content = event_description
	new_post.post_type = "event"
	new_post.post_status = "publish"
	new_post.terms_names = { 'event-category': [event_category] }
	new_post.custom_fields = []
	
	meta_adds = (['imic_event_start_dt',start_event],
				['imic_event_end_dt',end_event],
				['imic_event_frequency_end',end_frequency_event],
				['imic_featured_event','no'],
				['slide_template','default'],
				['imic_event_day_month','first'],
				['imic_event_week_day','sunday'],
				['imic_event_frequency_type','0'],
				['imic_event_frequency','35'],
				['imic_event_registration','0'],
				['imic_custom_event_registration_target','0'],
				['imic_sidebar_columns_layout','3'],
				['imic_google_map_track','1'],
				['imic_event_address2','Tananger kirke, Sola, Norway'],
				['imic_event_map_location','58.93535599999999,5.600313000000028'],
				['imic_pages_banner_overlay','0'],
				['imic_pages_banner_animation','0'],
				['imic_pages_select_revolution_from_list','[rev_slider fsl]'],
				['imic_pages_slider_pagination','no'],
				['imic_pages_slider_auto_slide','no'],
				['imic_pages_slider_direction_arrows','no'],
				['imic_pages_slider_interval','7000'],
				['imic_pages_slider_effects','fade'],
				['imic_pages_nivo_effects','sliceDown'])

	#Iterate over array creating meta in post
	for i in meta_adds:
		new_post.custom_fields.append({'key':i[0], 'value':i[1]})
				
	#Add New Post and it's meta data
	logging.info('Create a new WordPressPost - Title: [' + new_post.title + '] Starts: [' + start_event + '] Ends: [' + end_event + ']')
	if not dry_run:
		client.call(NewPost(new_post))


def create_all_posts_from_ical(client, ical, event_category, dry_run):
	"""Create new WordPress posts from ICalendar object"""

	i=0
	for component in ical.walk('VEVENT'):
		create_new_wp_post(client, component, event_category, dry_run)
		i += 1
	logging.info('Created %s WordPress posts',i)


def main():
	"""main function"""
	
	#Logging
	logging.basicConfig(filename='import_events.log', level=logging.INFO)
	logging.info('[START IMPORT]')
	
	#Populate the configs
	parser = populate_configs()
	
	#Config header name
	section = "config"
	ics_url = parser.get(section,'ics_url')
	wp_url = parser.get(section,'wp_url')
	ics_filename = parser.get(section,'ics_filename')
	wp_user = parser.get(section,'wp_user')
	wp_pwd = parser.get(section,'wp_pwd')
	event_category = parser.get(section,'event_category')
	dry_run = parser.get(section,'dry_run')

	if dry_run:
		logging.info('It\'s a DRY run');
	
	#Export the ICS file
	export_ics_file(ics_url, ics_filename)
	
	#Initate WordPress Client
	client = get_wordpress_client(wp_url, wp_user, wp_pwd)
	
	#Getting all IDs to delete
	ids = get_all_ids(client,event_category)
	
	#Delete wordpress posts
	delete_wp_posts(client, ids, dry_run)
	
	#Get the new Calendar
	cal = read_ical_file(ics_filename)
	
	#Create new posts
	create_all_posts_from_ical(client, cal, event_category, dry_run)
	
	#
	logging.info('[END IMPORT]')
    
#############
#Execute main
if __name__ == '__main__':
    main()
