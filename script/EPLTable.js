//table
cursor = db.games.aggregate
			( [ 
				//match EPL games 
				{ $match: { competition: "E0", $and: [ { gameDate: { $gt: ISODate("2015-08-01") } },  { gameDate: { $lt: ISODate("2016-06-01") }  } ] } }
				// unwinding every team is one row now
				,{ $unwind: { path: "$teams", includeArrayIndex: "HomeAway" } }
				// count games : Played, Won, Drawn, Lost; calculates goals : For, Against 
				,{ $group: 
					{ 
						_id :  "$teams",
						P : { $sum : 1 }, //games played
						W : { $sum : { $cond: {	if: { $or : [ 
															{ $and : [ { $eq : ['$matchResult.fullTimeResult', 'H'] }, { $eq : ['$HomeAway', 0] } ] }, 
															{ $and : [ { $eq : ['$matchResult.fullTimeResult', 'A'] }, { $eq : ['$HomeAway', 1] } ] }
															]
													}, 
												then: 1, else: 0 } } },
						D : { $sum : { $cond: { if: { $eq : ['$matchResult.fullTimeResult', 'D']}, then: 1, else: 0 } } },
						L : { $sum : { $cond: {	if: { $or : [ 
															{ $and : [ { $eq : ['$matchResult.fullTimeResult', 'A'] }, { $eq : ['$HomeAway', 0] } ] }, 
															{ $and : [ { $eq : ['$matchResult.fullTimeResult', 'H'] }, { $eq : ['$HomeAway', 1] } ] }
															]
													}, 
												then: 1, else: 0 } } },
						F : { $sum : { $cond: ["$HomeAway", "$matchResult.FTAG" , "$matchResult.FTHG"] } } ,
						A : { $sum : { $cond: ["$HomeAway", "$matchResult.FTHG" , "$matchResult.FTAG"] } } 
					}
				}
				//projection calculates : Points, GoalDifference, PointsPerGame
				,{ $project :
					{
						P : 1,
						W : 1,
						D : 1,
						L : 1,
						F : 1,
						A : 1,
						GD : {$subtract: [ "$GS", "$GC" ]},
						Pts : {$sum : {$add: [ {$multiply : [ "$W", 3 ] }, "$D" ]}},
						PPG : { $divide : [{$sum : {$add: [ {$multiply : [ "$W", 3 ] }, "$D" ]}}, "$P" ] }
					}
				}
				, { $sort : { Points : -1, GD : -1, GS : -1, W : -1, _id : 1 } }
					
			] )

while ( cursor.hasNext() ) {
   printjson( cursor.next() );
}

