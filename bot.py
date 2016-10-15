from physics import Physics

class Bot(Physics):
	def __init__(self, scale, x, y, canvas):
		Physics.__init__(self, scale, x, y)
		self.canvas = canvas
		self.character = self.canvas.create_oval(x-5, y-5, x+5, y+5, outline='white', fill='blue')
		self.canvas.pack()

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


	def animate(self):
		self.move()
		self.canvas.after(10, self.animate)

from Tkinter import *

root = Tk()
canvas = Canvas(root, width=400, height = 400)
canvas.pack()
bot = Bot(100, 55, 15, canvas)
bot.add_fx(1)
bot.add_fy(1)
bot.animate()
root.mainloop()
