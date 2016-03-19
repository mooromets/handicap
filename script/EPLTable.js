// HOME GAMES table
cursor = db.games.aggregate
			( [ 
				// unwinding every team is one row now
				{ $unwind: { path: "$teams", includeArrayIndex: "HomeAway" } }
				//match EPL and home games only 				,{ $match: { competition : "E0" , HomeAway : 0 } }
/*				
				,{ $project :
					{
						$let : {
							vars : {
							},
							in : {}
						}//let
					}
				}
*/				
				,{ $group: 
					{ 
//						_id :  {team: "$teams", host: "$HomeAway"},
						_id :  "$teams",
						G : { $sum : 1 },
						W : { $sum : { $cond: { if: { $or : [ 
															{ $and : [ { $eq : ['$matchResult.fullTimeResult', 'H'] }, { $eq : ['$HomeAway', 0] } ] }, 
															{ $and : [ { $eq : ['$matchResult.fullTimeResult', 'A'] }, { $eq : ['$HomeAway', 1] } ] }
															]
															}, then: 1, else: 0 } } },
						D : { $sum : { $cond: { if: { $eq : ['$matchResult.fullTimeResult', 'D']}, then: 1, else: 0 } } },
						L : { $sum : { $cond: { if: { $or : [ 
															{ $and : [ { $eq : ['$matchResult.fullTimeResult', 'A'] }, { $eq : ['$HomeAway', 0] } ] }, 
															{ $and : [ { $eq : ['$matchResult.fullTimeResult', 'H'] }, { $eq : ['$HomeAway', 1] } ] }
															]
															}, then: 1, else: 0 } } },
						GS : { $sum : { $cond: ["$HomeAway", "$matchResult.fullTimeScore.1" , "$matchResult.fullTimeScore.0"] } },
						GC : { $sum : { $cond: ["$HomeAway", "$matchResult.fullTimeScore.0" , "$matchResult.fullTimeScore.1"] } } 
					}
				}
				,{ $project :
					{
//						_id : {team : "$_id.team", side: {$cond: ["$HomeAway", "Aw", "Ho"] } },
						G : 1,
						W : 1,
						D : 1,
						L : 1,
						GS : 1,
						GC : 1,
						GD : {$subtract: [ "$GS", "$GC" ]},
						Points : {$sum : {$add: [ {$multiply : [ "$W", 3 ] }, "$D" ]}}
					}
				}
				, { $sort : { Points : -1, W : -1, _id : 1 } }
					
			] )

while ( cursor.hasNext() ) {
   printjson( cursor.next() );
}

