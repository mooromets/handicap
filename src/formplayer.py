import mongoQueries
from player import Player
from utils import printTable
from datetime import datetime

class FormPlayer (Player) :
	def __init__ (self, mongoConnection):
		Player.__init__(self, mongoConnection)

	def play (self, match, results):
		#temporary hard-code this season and league
		PL = "E0"
		startPL = datetime(2015, 8, 1)
		endPL = datetime(2016, 6, 1)
		
		endDate = match['gameDate'] if match['gameDate'] < endPL else endPL
		
		#prepare context
		
		tableCollection = "leagueTable"
		self.myMongoConn.db[tableCollection].drop()
		formCollection = "leagueForm"
		self.myMongoConn.db[formCollection].drop()
		
		#home games
		pipePLHome = mongoQueries.pipeLeagueTable(PL, startPL, endDate, True)
		pipePLHome.append( { "$out" : tableCollection } )
		self.myMongoConn.collTest.aggregate(pipePLHome) 

		#away games
		pipePLAway = mongoQueries.pipeLeagueTable(PL, startPL, endDate, False)
		for doc in list(self.myMongoConn.collTest.aggregate(pipePLAway)):	
			self.myMongoConn.db[tableCollection].insert_one(doc)
		
		#debug printTable(self.myMongoConn.db[tableCollection])
		
		#calculate form for both teams
		#refactor this shit
		matchTeamLimit = mongoQueries.matchLeagueTerm(PL, startPL, endDate)
		matchTeamLimit["$match"]["teams.0"] = match['teams'][0]

		pipeStats = lambda isHome: [
			matchTeamLimit,
			{ "$sort": { "gameDate" : -1 } },
			{ "$limit" : 6 },
			{ "$unwind": { "path": "$teams", "includeArrayIndex": "Ground" } },
			{ "$match": {"Ground": 0 if isHome else 1 } },
			mongoQueries.groupResultsAndGoals(isHome),
			mongoQueries.projectTableView()
		]
		
		homeTeamFormDoc = list(self.myMongoConn.collTest.aggregate(pipeStats(True)))[0]
#		for doc in list(self.myMongoConn.collTest.aggregate(pipeStats(True))): self.myMongoConn.db[formCollection].insert_one(doc)		
		
		matchTeamLimit = mongoQueries.matchLeagueTerm(PL, startPL, endDate)
		matchTeamLimit["$match"]["teams.1"] = match['teams'][1]
		
		awayTeamFormDoc = list(self.myMongoConn.collTest.aggregate(pipeStats(False)))[0]
#		for doc in list(self.myMongoConn.collTest.aggregate(pipeStats(False))): self.myMongoConn.db[formCollection].insert_one(doc)	

		#debug printTable(self.myMongoConn.db[formCollection])
		#print (homeTeamFormDoc)
		#print (awayTeamFormDoc)
		
		results.append( { 
							"PtsDiff": homeTeamFormDoc["Pts"] - awayTeamFormDoc["Pts"], 
							"Res": match['matchResult']['fullTimeResult'], 
							"odds": { 
										"H": match['bets']['BetbrainAvgH'],
										"D": match['bets']['BetbrainAvgD'],
										"A": match['bets']['BetbrainAvgA']
									}  
						} )