#!/usr/bin/python

from datetime import datetime
from icalendar import Calendar, vDDDTypes, Event
import subprocess, shlex

#DELETE ALL POSTS/EVENTS
print ("Deleting all posts");

#Getting all IDes to delete first
ider = subprocess.check_output(["./wp","post","list","--post_type=event","--format=ids"])
#If any id's was returned delete
if ider:
	#Use shlex.split to create a complex command with all ids
	kommando = "./wp post delete --force " + ider
	subprocess.Popen(shlex.split(kommando))

#OPEN ICS FILE
cal = Calendar.from_ical(open('./test.ics','rb').read())

for component in cal.walk('VEVENT'):	
	summary = component.get('SUMMARY').encode('UTF-8','backslashreplace')
	start_event = component.get('DTSTART').dt.strftime('%Y-%m-%d %H:%M')
	end_event = component.get('DTEND').dt.strftime('%Y-%m-%d %H:%M')	
	end_frequency_event = component.get('DTEND').dt.strftime('%Y-%m-%d')	
	event_description = component.get('DESCRIPTION').encode('UTF-8','backslashreplace')
	
	#NEW POST
	newpost_id = subprocess.check_output(["./wp","post","create","--post_type=event","--post_title=" + summary ,"--post_content="+event_description,"--post_status=publish","--porcelain"])
	print("Create new post -> " + summary + " " + newpost_id)
	subprocess.check_output(["./wp","post","term","set","--skip-themes=false",newpost_id,"event-category","gudstjeneste"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_event_start_dt",start_event])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_event_end_dt",end_event])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_event_frequency_end",end_frequency_event])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_featured_event","no"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"slide_template","default"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_event_day_month","first"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_event_week_day","sunday"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_event_frequency_type","0"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_event_frequency","35"])	
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_event_registration","0"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_custom_event_registration_target","0"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_sidebar_columns_layout","3"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_google_map_track","1"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_event_address2","Tananger kirke, Sola, Norway"])	
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_event_map_location","58.93535599999999,5.600313000000028"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_pages_banner_overlay","0"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_pages_banner_animation","0"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_pages_select_revolution_from_list","[rev_slider fsl]"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_pages_slider_pagination","no"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_pages_slider_auto_slide","no"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_pages_slider_direction_arrows","no"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_pages_slider_interval","7000"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_pages_slider_effects","fade"])
	subprocess.check_output(["./wp","post","meta","add",newpost_id,"imic_pages_nivo_effects","sliceDown"])

