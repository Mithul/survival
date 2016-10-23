# obstacle_food.py
class Food(object):
	def __init__(self, x, y, health_regen, health, canvas = None):
		self.x = x
		self.y = y
		self.health_regen = health_regen
		self.health = health
		if canvas:
			self.character = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline='white', fill=color)

	def get_eaten(bot):
		if self.health > 0:
			bot.health = bot.health + self.health_regen
			self.health = self.health - self.health_regen
		if self.health < 0:
			self.canvas.delete(self.character)