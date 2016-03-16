import csv
import pymongo

def insertFileIntoDB (inFilename, collection):
	csvFile = open(inFilename, 'r')
	header = csvFile.readline().split(',') # read first line as table header
	
	nInserted = 0
	csvReader = csv.DictReader( csvFile, header)
	for row in csvReader:
		data = {
				"gameDate" : row['Date'],
				"competition" : row['Div'],
				"referee" : row['Referee'],
				"teams" : [row['HomeTeam'], row['AwayTeam']],
				"matchResult" : 
				{
					"fullTimeScore" : [row['FTHG'], row['FTAG']],
					"fullTimeResult" : row['FTR'],
					"halfTimeScore" : [row['HTHG'], row['HTAG']],
					"halfTimeResult" : row['HTR']
				},
				"matchStats" : 
				{
					"HomeTeamShots" : row["HS"],
					"AwayTeamShots" : row["AS"],
					"HomeTeamShotsTarget" : row["HST"],
					"AwayTeamShotsTarget": row["AST"],
					"HomeTeamYellowCards": row["HY"],
					"AwayTeamYellowCards": row["AY"],
					"HomeTeamRedCards": row["HR"],
					"AwayTeamRedCards": row["AR"]
				},
				"bets" : 
				{
					"Bet365H" : row["B365H"],
					"Bet365D" : row["B365D"],
					"Bet365A" : row["B365A"],
					"BetbrainMaxH" : row["BbMxH"],
					"BetbrainAvgH" : row["BbAvH"],
					"BetbrainMaxD" : row["BbMxD"],
					"BetbrainAvgD" : row["BbAvD"],
					"BetbrainMaxA" : row["BbMxA"],
					"BetbrainAvgA" : row["BbAvA"],
					"BetbrainMaxGr25" : row["BbMx>2.5"],
					"BetbrainAvgGr25" : row["BbAv>2.5"],
					"BetbrainMaxLe25" : row["BbMx<2.5"],
					"BetbrainAvgLe25" : row["BbAv<2.5"]
				}
				}
		if collection.insert_one(data).acknowledged : nInserted += 1
	return nInserted
