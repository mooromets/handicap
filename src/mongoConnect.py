import pymongo

from pymongo import MongoClient

class HandiMongo:
	def __init__(self, user, pswd):
		self.client = MongoClient('mongodb://'+ user +':'+ pswd +'@ds054128.mlab.com:54128/handicap')
		print "connected to ds054128.mlab.com"
		self.db = self.client.handicap
		print "db set handicap"		
		self.collTest = self.db.testCollection
		print "testCollection set"		
		