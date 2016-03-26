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
			#print (team)
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
							"Club": doc['teams'][oppIdx],
							"Ground": 'A'
						} )
				oppPPG = oppLeagueDoc['Pts'] / oppLeagueDoc['P']
				formPoints[teamIdx] = formPoints[teamIdx] + self.points(teamIdx, doc["matchResult"]["fullTimeResult"])
				accFormPonits[teamIdx] = accFormPonits[teamIdx] + self.points(teamIdx, doc["matchResult"]["fullTimeResult"]) * oppPPG
				#print (oppLeagueDoc['Club'], teamIdx, oppPPG, self.points(teamIdx, doc["matchResult"]["fullTimeResult"]))
				
			#print (accFormPonits[teamIdx])
		
		
#		for doc in list(self.myMongoConn.collTest.aggregate(pipeStats(False))): self.myMongoConn.db[formCollection].insert_one(doc)	

		#debug printTable(self.myMongoConn.db[formCollection])
		#print (homeTeamFormDoc)
		#print (awayTeamFormDoc)
		
		if match['matchResult']['fullTimeResult'] == 'D': 
			finalRes = "bD"
			resOdd = match['bets']['BetbrainAvgD']
		elif match['matchResult']['fullTimeResult'] == 'H' and accFormPonits[0] > accFormPonits[1]:
			finalRes = "cW"
			resOdd = match['bets']['BetbrainAvgH']
		elif match['matchResult']['fullTimeResult'] == 'A' and accFormPonits[1] > accFormPonits[0]:
			finalRes = "cW"
			resOdd = match['bets']['BetbrainAvgA']		
		elif match['matchResult']['fullTimeResult'] == 'H' and accFormPonits[0] < accFormPonits[1]:
			finalRes = "aL"
			resOdd = match['bets']['BetbrainAvgH']
		elif match['matchResult']['fullTimeResult'] == 'A' and accFormPonits[1] < accFormPonits[0]:
			finalRes = "aL"
			resOdd = match['bets']['BetbrainAvgA']	
		else:
			finalRes = "bD_unk"
			resOdd = match['bets']['BetbrainAvgD']	
		
		results.append( { 
							"PtsDiff": fabs (formPoints[0] - formPoints[1]),
							"AccDiff": fabs (accFormPonits[0] - accFormPonits[1]),
							"Res": finalRes,
							"WinOdd" : resOdd,
							"odds": { 
										"H": match['bets']['BetbrainAvgH'],
										"D": match['bets']['BetbrainAvgD'],
										"A": match['bets']['BetbrainAvgA']
									},
							"AccHome" : accFormPonits[0],
							"AccAway" : accFormPonits[1],
						} )