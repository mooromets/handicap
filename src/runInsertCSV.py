import sys

import mongoConnect
import mongoInsertData

#open MongoDB connection

collectionName = sys.argv[2] if len(sys.argv)>2 else 'games'

hm = mongoConnect.HandiMongo(collectionName)

#open input file
csvName = sys.argv[1] if len(sys.argv)>1 else 'input.csv'
print (mongoInsertData.insertFileIntoDB(csvName, hm.collTest))
