#!/usr/bin/python

#https://python-wordpress-xmlrpc.readthedocs.org/
#https://github.com/maxcutler/python-wordpress-xmlrpc.git
#https://github.com/collective/icalendar
#dependent on pytz
#pip install pytz
from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import GetPosts, NewPost, DeletePost
from wordpress_xmlrpc.methods.users import GetUserInfo
from datetime import datetime
from icalendar import Calendar, vDDDTypes, Event
from subprocess import check_output
import ConfigParser, os
import sys

#CONFIGS
section = "config"

#Get config file to read
if len(sys.argv)<=1:
	print "No config file"
	sys.exit(2)

cfgfilename = sys.argv[1]
if not os.path.isfile(cfgfilename):
	print "File not found: " + cfgfilename
	sys.exit(2)

print "Read configs"
parser = ConfigParser.ConfigParser();
parser.readfp(open(cfgfilename))

medarb_ics_url = parser.get(section,'ics_url')
wp_url = parser.get(section,'wp_url')
gudstjenester_ics = parser.get(section,'ics_filename')
wp_user = parser.get(section,'wp_user')
wp_pwd = parser.get(section,'wp_pwd')
event_category = parser.get(section,'event_category')


#EXPORT ICS
print "Get ICS file -> " + medarb_ics_url
export_ics = check_output(["curl","--silent",medarb_ics_url])
if export_ics:
	f = open(gudstjenester_ics,'w')
	f.write(export_ics)
	f.close()


#New WordPress object
print "Get a WordPress instance"
wp = Client(wp_url + '/xmlrpc.php', wp_user, wp_pwd)

#Get all IDs of Posts of post_type 'event'
print "Get all posts with category-event " + event_category + " and delete those"
offset = 0
increment = 10
ids = []
while True:
	posts = wp.call(GetPosts({'post_type': 'event', 'number': increment, 'offset': offset}))
	if len(posts) == 0:
		break #no more posts
	for one_post in posts:		
		if (one_post.terms[0].name == event_category):
			ids.append(one_post.id)
	offset += increment


#Iterate and delete posts
for delete_id in ids:
	print "Deleteing id -> " + delete_id
	wp.call(DeletePost(delete_id))


#OPEN ICS FILE
print "Read ICAL file"
cal = Calendar.from_ical(open(gudstjenester_ics,'rb').read())
for component in cal.walk('VEVENT'):	
	summary = component.get('SUMMARY').encode('UTF-8','backslashreplace')
	start_event = component.get('DTSTART').dt.strftime('%Y-%m-%d %H:%M')
	end_event = component.get('DTEND').dt.strftime('%Y-%m-%d %H:%M')	
	end_frequency_event = component.get('DTEND').dt.strftime('%Y-%m-%d')	
	event_description = component.get('DESCRIPTION').encode('UTF-8','backslashreplace')
	
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
	print "Create new post -> " + new_post.title
	wp.call(NewPost(new_post))
