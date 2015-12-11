#!/usr/bin/python

from datetime import datetime
from icalendar import Calendar, vDDDTypes, Event
import subprocess, shlex, array

#Variabler
gudstjenester_ics = "events.ics"
medarb_ics_url = "https://wsu4.mylabora.com/churchhubrelease/icalhandler.ashx?iCal=8fa0ae2d-2380-400b-9960-a56500bfaf87"
wp_cmd = "./wp"

#DELETE ALL POSTS/EVENTS
print ("Deleting all posts");

#Getting all IDes to delete first
ider = subprocess.check_output([wp_cmd,"post","list","--post_type=event","--format=ids"])
#If any id's was returned delete
if ider:
	#Use shlex.split to create a complex command with all ids
	kommando = wp_cmd + " post delete --force " + ider
	subprocess.Popen(shlex.split(kommando))


#EXPORT ICS
export_ics = subprocess.check_output(["curl","--silent",medarb_ics_url])
if export_ics:
	f = open(gudstjenester_ics,'w')
	f.write(export_ics)
	f.close()

#OPEN ICS FILE
cal = Calendar.from_ical(open(gudstjenester_ics,'rb').read())
for component in cal.walk('VEVENT'):	
	summary = component.get('SUMMARY').encode('UTF-8','backslashreplace')
	start_event = component.get('DTSTART').dt.strftime('%Y-%m-%d %H:%M')
	end_event = component.get('DTEND').dt.strftime('%Y-%m-%d %H:%M')	
	end_frequency_event = component.get('DTEND').dt.strftime('%Y-%m-%d')	
	event_description = component.get('DESCRIPTION').encode('UTF-8','backslashreplace')
	
	#LAG ARRAY
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
	

	#NEW POST
	newpost_id = subprocess.check_output([wp_cmd,"post","create","--post_type=event","--post_title=" + summary ,"--post_content="+event_description,"--post_status=publish","--porcelain"])
	print("Create new post -> " + summary + " " + newpost_id)
	subprocess.check_output([wp_cmd,"post","term","set","--skip-themes=false",newpost_id,"event-category","gudstjeneste"])
	
	#Iterate over array creating meta in post
	for i in meta_adds:
		subprocess.check_output([wp_cmd,"post","meta","add",newpost_id,i[0],i[1]])
