class Walker:
	def __init__ (self, games, player, results):
		for game in games:
			player.play(game, results)
