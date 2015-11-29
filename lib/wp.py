#!/usr/bin/python

import MySQLdb
import ConfigParser, os

class WPSql:
	
	
		def __init__(self):

			section = "db"
			parser = ConfigParser.ConfigParser();					
			
			try:
				parser.readfp(open(self.cfgfilename))
				self.db = MySQLdb.connect(parser.get(section,'host'),parser.get(section,'user'),parser.get(section,'password'), parser.get(section,'dbname') )
				self.cursor = self.db.cursor()							
			except Exception as e:
				print ("Error : ", e)
				raise				
			
		def retrieve(self, sql):
						
			self.cursor.execute(sql);
			self.results = self.cursor.fetchall()
			return self.results

		def __del__(self):
			self.db.close()
			print 'Closed db'



class WPPost:	

	def __init__(self):
		self.ID = 0

	def getID(self):
		return self.ID

	def getType(self):
		return self.postType

	def setPost(self, ID, author, date, date_gmt, content):
		self.ID = ID
		self.author = author
		self.date = date
		self.dateGmt = date_gmt
		self.content = content


class Sermon(WPPost):

	postType = "sermon"

	def __init__(self):
		wpsql = WPSql()
		result = wpsql.retrieve("select id, post_author, post_date, post_date_gmt, post_content from wp_posts where post_type = 'post'")
		for row in result:
			self.setPost(row[0],row[1],row[2],row[3],row[4]);
			

	def __str__(self):
		return "From str method of Sermon: ID is %s, post_author is %s " % (self.ID, self.author)
