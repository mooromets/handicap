import csv
import pymongo
from datetime import datetime

def insertFileIntoDB (inFilename, collection):
	csvFile = open(inFilename, 'r')
	header = csvFile.readline().split(',') # read first line as table header
	
	nInserted = 0
	csvReader = csv.DictReader( csvFile, header)
	for row in csvReader:
		data = {
				"gameDate" : datetime.strptime(row['Date'], "%d/%m/%y"),
				"competition" : row['Div'],
				"referee" : row['Referee'],
				"teams" : [row['HomeTeam'], row['AwayTeam']],
				"matchResult" : 
				{
					"FTHG" : int( row['FTHG'] ),
					"FTAG" : int( row['FTAG'] ),
					"HTHG" : int( row['HTHG'] ),
					"HTAG" : int( row['HTAG'] ),
					"fullTimeResult" : row['FTR'],
					"halfTimeResult" : row['HTR']
				},
				"matchStats" : 
				{
					"HomeTeamShots" : int( row["HS"] ),
					"AwayTeamShots" : int( row["AS"] ),
					"HomeTeamShotsTarget" : int( row["HST"] ),
					"AwayTeamShotsTarget": int( row["AST"] ),
					"HomeTeamYellowCards": int( row["HY"] ),
					"AwayTeamYellowCards": int( row["AY"] ),
					"HomeTeamRedCards": int( row["HR"] ),
					"AwayTeamRedCards": int( row["AR"] )
				},
				"bets" : 
				{
					"Bet365H" : float( row["B365H"] ),
					"Bet365D" : float( row["B365D"] ),
					"Bet365A" : float( row["B365A"] ),
					"BetbrainMaxH" : float( row["BbMxH"] ),
					"BetbrainAvgH" : float( row["BbAvH"] ),
					"BetbrainMaxD" : float( row["BbMxD"] ),
					"BetbrainAvgD" : float( row["BbAvD"] ),
					"BetbrainMaxA" : float( row["BbMxA"] ),
					"BetbrainAvgA" : float( row["BbAvA"] ),
					"BetbrainMaxGr25" : float( row["BbMx>2.5"] ),
					"BetbrainAvgGr25" : float( row["BbAv>2.5"] ),
					"BetbrainMaxLe25" : float( row["BbMx<2.5"] ),
					"BetbrainAvgLe25" : float( row["BbAv<2.5"] )
				}
				}
		if collection.insert_one(data).acknowledged : nInserted += 1
	return nInserted
