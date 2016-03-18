import pymongo

from pymongo import MongoClient

class HandiMongo:
	def __init__(self, user, pswd): # user, pswd are ignored when local
		#self.client = MongoClient('mongodb://'+ user +':'+ pswd +'@ds054128.mlab.com:54128/handicap')
		self.client = MongoClient()
		print "connected to local"
		self.db = self.client.foot
		print "db set foot"		
		self.collTest = self.db.games
		print "collection games is set"		
		