import sys
import csv

import mongoConnect
import mongoInsertData

from formplayer import FormPlayer
from walker import Walker
from datetime import datetime
from datetime import time

#open MongoDB connection

collectionName = sys.argv[2] if len(sys.argv)>2 else 'games'

hm = mongoConnect.HandiMongo(collectionName)

#open input file
#csvName = sys.argv[1] if len(sys.argv)>1 else 'input.csv'
#print (mongoInsertData.insertFileIntoDB(csvName, hm.collTest))

PL = "E0"
start = datetime(2015, 10, 18)
end = datetime(2016, 6, 1)

queryFind = { 
	"competition": "E0",
	"$and" : 
		[
			{"gameDate": { "$gte" : start } }, 
			{"gameDate": { "$lt" : end } } 
		]
} 

check = list(hm.collTest.find(queryFind))

#for doc in check: print (doc)
	
fp = FormPlayer(hm)	

results = []

print ("Start Walker")
timer = datetime.now()

walk = Walker(check, fp, results)

print ("Walker ends")
print ("Lasted:", ( datetime.now() - timer).microseconds )

print(len(results))

for doc in results: 
	print (doc["PtsDiff"], doc["Res"], doc["odds"][doc["Res"]], doc["odds"]["H"], doc["odds"]["D"], doc["odds"]["A"])
