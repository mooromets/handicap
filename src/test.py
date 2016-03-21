import mongoConnect
from datetime import datetime

import mongoQueries
#open MongoDB connection


hm = mongoConnect.HandiMongo("games")

pipeline = [
	mongoQueries.matchLeagueTerm("E0", datetime(2015, 8, 1), datetime(2016, 6, 1)),
	{ "$unwind" : { "path": "$teams", "includeArrayIndex": "HomeAway" } },
	{ "$group" : { "_id" : "$teams" } }
]

newColPipeline = list(mongoQueries.LeagueTablePipeine)
newColPipeline.append( { "$out" : "leagueTable" } )

for doc in list(hm.collTest.aggregate(newColPipeline)):
	print (doc)


