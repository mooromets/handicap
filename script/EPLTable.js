// HOME GAMES table
cursor = db.games.aggregate
			( [ 
				// unwinding every team is one row now
				{ $unwind: { path: "$teams", includeArrayIndex: "HomeAway" } }
				//match EPL and home games only
				,{ $match: { competition : "E0" , HomeAway : 0 } }
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
						_id :  "$teams",
						G : { $sum : 1 },
						W : { $sum : { $cond: { if: { $eq : ['$matchResult.fullTimeResult', 'H']}, then: 1, else: 0 } } },
						D : { $sum : { $cond: { if: { $eq : ['$matchResult.fullTimeResult', 'D']}, then: 1, else: 0 } } },
						L : { $sum : { $cond: { if: { $eq : ['$matchResult.fullTimeResult', 'A']}, then: 1, else: 0 } } },
						Points : {$sum : {$add: [ {$multiply : [ { $cond: { if: { $eq : ['$matchResult.fullTimeResult', 'H']}, then: 1, else: 0 } }, 3 ] }, { $cond: { if: { $eq : ['$matchResult.fullTimeResult', 'D']}, then: 1, else: 0 } } ]}}
					}
				}
					
			] )

while ( cursor.hasNext() ) {
   printjson( cursor.next() );
}

