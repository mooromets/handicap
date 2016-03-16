import sys
import csv

import mongoConnect
import mongoInsertData

#open MongoDB connection

if len(sys.argv) < 3: 
	print "user and password must be specified"
	exit()
hm = mongoConnect.HandiMongo(sys.argv[1], sys.argv[2])

#open input file

csvName = sys.argv[3] if len(sys.argv)>3 else 'input.csv'

print mongoInsertData.insertFileIntoDB(csvName, hm.collTest)