import mongoQueries

#utils

def printTable (table):

	template = "{:15}| {:2}| {:2}-{:2}-{:2}| {:3}-{:3} {:3}| {:3}"
	header = template.format ("Club", "P", "W", "D", "L", "F", "A", "GD", "Pts")
	print ("\n" + header)
	
	pipe = 	[
			{"$group": {	"_id": "$Club",
							"P" : { "$sum": "$P" }, 
							"W" : { "$sum": "$W" },
							"D" : { "$sum": "$D" },
							"L" : { "$sum": "$L" },
							"F" : { "$sum": "$F" },
							"A" : { "$sum": "$A" },
							"GD" : { "$sum": "$GD" },
							"Pts" : { "$sum": "$Pts" } }						
			}
	]
	for team in list(table.aggregate(pipe)):
		print (template.format(	team['_id'], team['P'],	team['W'],
								team['D'], team['L'], team['F'],
								team['A'], team['GD'], team['Pts']))