from Tkinter import *
import time
from bot import Bot

def animator(bots):
	collision_check = {}
	for bot in bots:
		collision_check[bot] = []
		for bot1 in bots:
			if bot==bot1:
				continue
			if (bot in collision_check and (bot1 in collision_check[bot])) or (bot1 in collision_check and (bot in collision_check[bot1])):
				continue
			collision_check[bot].append(bot1)
			c = bot.collision_detect(bot1)
			if c:
				pass
				# print bot.name, bot1.name
		bot.animate()
	canvas.after(10, animator,bots)
import tensorflow as tf
import numpy as np
sess = tf.Session()
def test(bots):
	nn_input = []
	for bot in bots:
		surr = bot.surroundings(bots)
		nn_input = [[bot.velx, bot.vely, bot.fx, bot.fy, bot.health/100, surr['l'], surr['u'], surr['r'], surr['d']]]
		res = sess.run([bot.thrusters], {bot.input_nn: nn_input})
		bot.add_fx(res[0][0][0])
		bot.add_fy(res[0][0][1])
		if bot.collisions > 0:
			nn_input = [[bot.velx, bot.vely, bot.fx, bot.fy, bot.health/100, surr['l'], surr['u'], surr['r'], surr['d']]]
			import pdb
			res = sess.run([bot.thrusters, bot.train_step, bot.loss, bot.input_nn], {bot.input_nn: nn_input, bot.score: np.reshape(np.asarray([-bot.fx, -bot.fy]),[-1,2])})
			bot.add_fx(res[0][0][0])
			bot.add_fy(res[0][0][1])
			print bot.name, bot.collisions, res[0][0], res[2], res[3][0]
			bot.reset_collisions()
			
	canvas.after(100, test, bots)



root = Tk()
canvas = Canvas(root, width=400, height = 400)
canvas.pack()
import random
bots = []
for i in xrange(2):
	bot = Bot(40, i*90, 40, 50, canvas, str(i))
	bot.add_fx(0.1)
	bot.add_fy(0.1)
	bot.setup_nn()
	bots.append(bot)

sess.run(tf.initialize_all_variables())
animator(bots)
canvas.after(100, test, bots)
root.mainloop()