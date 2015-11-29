#!/usr/bin/python

import lib.wp 

#Specify config file with db property info
lib.wp.WPSql.cfgfilename = "config.cfg"


try:
	mySermon = lib.wp.Sermon()
	print "Sermon %s " % mySermon 
except Exception as e:
	print ("Stopping")

