import mongoConnect
from datetime import datetime
from bson.son import SON

def matchLeagueTerm(league, dateStart, dateEnd):
	return 	{ "$match":	{ 
							"competition": league, 
							"$and": [ 
									{ "gameDate": { "$gt": dateStart } }, 
									{ "gameDate": { "$lt": dateEnd } } 
									] 
						} 
			}

condAnd = lambda gr, idx: { "$and" : [ { "$eq": [ '$matchResult.fullTimeResult', gr ] }, { "$eq" : [ '$Ground', idx ] } ] }


def sortEPL():
	return { "$sort" : { "Pts" : -1, "GD" : -1, "GS" : -1, "W" : -1 } }

	
			
LeagueTablePipeine = [
	matchLeagueTerm("E0", datetime(2015, 8, 1), datetime(2016, 6, 1))
	,{ "$unwind": { "path": "$teams", "includeArrayIndex": "Ground" } }
	,{ "$group":
				{	
					"_id":  { "club": "$teams", "Ground" : "$Ground" },
					"P":	{ "$sum": 1 },
					"W":	{ "$sum": { "$cond":{	
												"if":	{ "$or": [ 
															condAnd('H', 0), 
															condAnd('A', 1)
															]
														}, 
												"then": 1, 
												"else": 0 
												} } 
							},
					"D":	{ "$sum": { "$cond":{
												"if": { "$eq" : [ '$matchResult.fullTimeResult', 'D' ] }, 
												"then": 1, 
												"else": 0 
												} } 
							},
					"L": 	{ "$sum": { "$cond":{
												"if": 	{ "$or" : [
															condAnd('A', 0), 
															condAnd('H', 1)						
															]
														}, 
												"then": 1, 
												"else": 0 
												} } 
							},
					"F": 	{ "$sum": { "$cond": ["$Ground", "$matchResult.FTAG" , "$matchResult.FTHG"] } } ,
					"A": 	{ "$sum": { "$cond": ["$Ground", "$matchResult.FTHG" , "$matchResult.FTAG"] } } 
					}
	}
	,{ "$project":
					{
						"Club" : "$_id.club",
						"Ground" : { "$cond": ["$_id.Ground", 'A' , 'H'] },
						"HA" : 1,
						"P" : 1,
						"W" : 1,
						"D" : 1,
						"L" : 1,
						"F" : 1,
						"A" : 1,
						"GD" : { "$subtract": [ "$GS", "$GC" ] },
						"Pts" : { "$sum" : { "$add": [ { "$multiply" : [ "$W", 3 ] }, "$D" ] } } 
#						PPG : { $divide : [{$sum : {$add: [ {$multiply : [ "$W", 3 ] }, "$D" ]}}, "$P" ] }
					}
	}	
]