import mongoQueries
from player import Player
from utils import printTable
from datetime import datetime
from mongoQueries import matchLeagueTerm

class FormPlayer (Player) :
	def __init__ (self, mongoConnection):
		Player.__init__(self, mongoConnection)
		self.mLastContextUpdate = datetime(1990, 1, 1)
		self.mLastGameDay = datetime(1990, 1, 1)
		#temporary hard-code this season and league
		self.mPL = "E0"
		self.mStartPL = datetime(2015, 8, 1)
		self.mEndPL = datetime(2016, 6, 1)
		self.mTeamsList = list(mongoConnection.collTest.aggregate([
							matchLeagueTerm(self.mPL, self.mStartPL, self.mEndPL),
							{ "$limit" : 50 },
							{ "$unwind": "$teams"},
							{ "$group" : { "_id": "$teams"}}
							]))
		print("fp inited")
		
	def prepareContext(self, match):
		needUpdate = True if (match['gameDate'] - self.mLastGameDay).days > 1 else False
		
		self.mLastGameDay = match['gameDate']

		if (match['gameDate'] - self.mLastContextUpdate).days > 3 : #many days of consecutive matches ?
			needUpdate = True
		
		if needUpdate :
			#print ("Update : ", match['gameDate'])
			self.mLastContextUpdate = match['gameDate']
		
			endDate = match['gameDate'] if match['gameDate'] < self.mEndPL else self.mEndPL	
			
			self.mTableCollection = "leagueTable"
			self.myMongoConn.db[self.mTableCollection].drop()
			self.mFormCollection = "leagueForm"
			self.myMongoConn.db[self.mFormCollection].drop()
			#home games
			pipePLHome = mongoQueries.pipeLeagueTable(self.mPL, self.mStartPL, endDate, True)
			pipePLHome.append( { "$out" : self.mTableCollection } )
			self.myMongoConn.collTest.aggregate(pipePLHome) 

			#away games
			pipePLAway = mongoQueries.pipeLeagueTable(self.mPL, self.mStartPL, endDate, False)
			for doc in list(self.myMongoConn.collTest.aggregate(pipePLAway)):	
				self.myMongoConn.db[self.mTableCollection].insert_one(doc)
			
			#debug printTable(self.myMongoConn.db[tableCollection])
		
		
	def play (self, match, results):

		self.prepareContext(match)
		
		endDate = match['gameDate'] if match['gameDate'] < self.mEndPL else self.mEndPL	
		
		#calculate form for both teams
		#refactor this shit
		matchTeamLimit = mongoQueries.matchLeagueTerm(self.mPL, self.mStartPL, endDate)
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
		
		matchTeamLimit = mongoQueries.matchLeagueTerm(self.mPL, self.mStartPL, endDate)
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