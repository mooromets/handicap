import mongoConnect
from datetime import datetime

import mongoQueries

#open MongoDB connection
hm = mongoConnect.HandiMongo("games")

# prepare competition context

PL = "E0"
startPL = datetime(2015, 8, 1)
endPL = datetime(2016, 6, 1)
collLeagueTable = "leagueTable"
hm.db[collLeagueTable].drop()
collLeagueForm = "leagueForm"
hm.db[collLeagueForm].drop()

#home games
pipePLHome = mongoQueries.pipeLeagueTable(PL, startPL, endPL, True)
pipePLHome.append( { "$out" : collLeagueTable } )
hm.collTest.aggregate(pipePLHome) 
#away games
pipePLHome = mongoQueries.pipeLeagueTable(PL, startPL, endPL, False)
for doc in list(hm.collTest.aggregate(pipePLHome)):	
	hm.db[collLeagueTable].insert_one(doc)

# major loop on all teams
pipeAllTeams = [
	{ "$unwind": "$teams" },
	mongoQueries.matchLeagueTerm(PL, startPL, endPL),
	{ "$group": { "_id": "$teams" } }
]

for team in list(hm.collTest.aggregate(pipeAllTeams)):
	print (team['_id'])
	
	#refactor this shit
	
	matchTeamLimit = mongoQueries.matchLeagueTerm(PL, startPL, endPL)
	matchTeamLimit["$match"]["teams.0"] = team['_id']

	pipeStats = lambda isHome: [
		matchTeamLimit,
		{ "$sort": { "gameDate" : -1 } },
		{ "$limit" : 6 },
		{ "$unwind": { "path": "$teams", "includeArrayIndex": "Ground" } },
		{ "$match": {"Ground": 0 if isHome else 1 } },
		mongoQueries.groupResultsAndGoals(isHome),
		mongoQueries.projectTableView()
	]
	
	for doc in list(hm.collTest.aggregate(pipeStats(True))):
		hm.db[collLeagueForm].insert_one(doc)

	matchTeamLimit = mongoQueries.matchLeagueTerm(PL, startPL, endPL)
	matchTeamLimit["$match"]["teams.1"] = team['_id']
		
	for doc in list(hm.collTest.aggregate(pipeStats(False))):
		hm.db[collLeagueForm].insert_one(doc)		
	