import sys
import csv

import mongoConnect
import mongoInsertData

from formplayer import FormPlayer
from walker import Walker
from datetime import datetime

#open MongoDB connection

collectionName = sys.argv[2] if len(sys.argv)>2 else 'games'

hm = mongoConnect.HandiMongo(collectionName)

#open input file
#csvName = sys.argv[1] if len(sys.argv)>1 else 'input.csv'
#print (mongoInsertData.insertFileIntoDB(csvName, hm.collTest))

PL = "E0"
start = datetime(2015, 9, 14)
end = datetime(2015, 9, 15)

queryFind = { 
	"competition": "E0",
	"$and" : 
		[
			{"gameDate": { "$gte" : start } }, 
			{"gameDate": { "$lt" : end } } 
		]
} 

check = list(hm.collTest.find(queryFind))

for doc in check:
	print (doc)
	
fp = FormPlayer(hm)	
	
walk = Walker(check, fp, True)


