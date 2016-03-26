import mongoQueries
from formplayer import FormPlayer
from utils import printTable
from datetime import datetime
from mongoQueries import matchLeagueTerm
from math import fabs

class FormPlayerAccelerated (FormPlayer) :
	def points (self, index, result):
		if index == 0 and result == 'H' or index == 1 and result == 'A':
			return 3
		elif result == 'D': 
			return 1
		else:
			return 0

	def play (self, match, results):

		self.prepareContext(match)
		
		endDate = match['gameDate'] if match['gameDate'] < self.mEndPL else self.mEndPL	
		
		#calculate form for both teams
		#refactor this shit
		

		
		formPoints = []
		accFormPonits = []
		
		for team in match['teams']:
			teamIdx = match['teams'].index(team)
			matchTeamLimit = mongoQueries.matchLeagueTerm(self.mPL, self.mStartPL, endDate)
			matchTeamLimit["$match"]["teams." + str(teamIdx)] = team
			pipeLastGames = [
				matchTeamLimit,
				{ "$sort": { "gameDate" : -1 } },
				{ "$limit" : 6 }
			]
			formPoints.append(0)
			accFormPonits.append(0.0)
		
			for doc in list(self.myMongoConn.collTest.aggregate(pipeLastGames)):
				#get PPG of the opponent
				oppIdx = 1 if teamIdx == 0 else 0
				oppLeagueDoc = self.myMongoConn.db[self.mTableCollection].find_one( 
						{ 
							"Club": match['teams'][oppIdx],
							"Ground": 'A'
						} )
				oppPPG = oppLeagueDoc['Pts'] / oppLeagueDoc['P']
				formPoints[teamIdx] = formPoints[teamIdx] + self.points(teamIdx, doc["matchResult"]["fullTimeResult"])
				accFormPonits[teamIdx] = accFormPonits[teamIdx] + self.points(teamIdx, doc["matchResult"]["fullTimeResult"]) * oppPPG
		
		
		
#		for doc in list(self.myMongoConn.collTest.aggregate(pipeStats(False))): self.myMongoConn.db[formCollection].insert_one(doc)	

		#debug printTable(self.myMongoConn.db[formCollection])
		#print (homeTeamFormDoc)
		#print (awayTeamFormDoc)
		
		results.append( { 
							"PtsDiff": fabs (formPoints[0] - formPoints[1]),
							"AccDiff": fabs (accFormPonits[0] - accFormPonits[1]),
							"Res": match['matchResult']['fullTimeResult'], 
							"odds": { 
										"H": match['bets']['BetbrainAvgH'],
										"D": match['bets']['BetbrainAvgD'],
										"A": match['bets']['BetbrainAvgA']
									},
							"AccHome" : accFormPonits[0],
							"AccAway" : accFormPonits[1],
						} )