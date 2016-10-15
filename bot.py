from physics import Physics
import math

class Bot(Physics):
	def __init__(self, x, y, radius, scale, canvas, name='1'):
		Physics.__init__(self, scale, x, y)
		self.canvas = canvas
		self.character = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline='white', fill='blue')
		self.canvas.pack()
		self.radius = radius
		self.name = name

	def move(self):
		old_pos = self.get_pos()

		if old_pos[0] > 400:
			self.collide(0)
		if old_pos[0] < 0:
			self.collide(180)
		if old_pos[1] > 400:
			self.collide(90)
		if old_pos[1] < 0:
			self.collide(-90)

		new_pos = Physics.move(self)
		self.canvas.move(self.character, new_pos[0] - old_pos[0], new_pos[1] - old_pos[1])
		self.canvas.update()

	def collision_detect(self, obj):
		if (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.radius + obj.radius)**2:
			rvx = obj.velx - self.velx
			rvy = obj.vely - self.vely
			angle = math.atan2(rvx, rvy)
			print math.degrees(angle), self.name, self.x, self.y, obj.name, obj.x, obj.y, (self.x - obj.x)**2 + (self.y - obj.y)**2
			# self.collide(math.degrees(angle))
			obj.collide(math.degrees(angle))
			# print angle
			return True
		else:
			return False


	def animate(self):
		self.move()
		# self.canvas.after(1000/60, self.animate)

from Tkinter import *
import time
root = Tk()
canvas = Canvas(root, width=400, height = 400)
canvas.pack()
import random
bots = []
for i in xrange(5):
	bot = Bot(random.randint(0,400), random.randint(0,400), 20, 100, canvas, str(i))
	bot.add_fx(random.random()*4-2)
	bot.add_fy(random.random()*4-2)
	bot.animate()
	bots.append(bot)


def animator(bots):
	for bot in bots:
		# for bot1 in bots:
		# 	if bot==bot1:
		# 		continue
		# 	c = bot.collision_detect(bot1)
		# 	if c:
		# 		print bot.name, bot1.name
		bot.animate()
	canvas.after(10, animator,bots)

animator(bots)
root.mainloop()
