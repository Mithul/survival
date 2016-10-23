from Tkinter import *
import time
from bot import Bot
import random

frame = 0
stopped = False
def animator(bots):
	global stopped
	global frame
	collision_check = {}
	restart = False
	bot_healths = ""
	if stopped:
		return
	for bot in bots:
		# if bot.health < 0:
		# 	continue
		restart = True
		# print ' bot '+bot.name, bot.health
		bot_healths = bot_healths + bot.name + ':' + "%7.2f"%bot.health + ' '
		collision_check[bot] = []
		for bot1 in bots:
			if bot1.health < 0:
				continue
			if bot==bot1:
				continue
			if (bot in collision_check and (bot1 in collision_check[bot])) or (bot1 in collision_check and (bot in collision_check[bot1])):
				continue
			collision_check[bot].append(bot1)
			c = bot.collision_detect(bot1)
			if c:
				pass
				# print bot.name, bot1.name
		surr = bot.surroundings(bots)
		nn_input = [[bot.velx, bot.vely, bot.fx, bot.fy, bot.health/100, surr['l'], surr['u'], surr['r'], surr['d']]]
		
		fx = 0
		fy = 0
		if random.random() > 0.5:
			score = [-1, 10, -1, -1, 10, -1]
			score = np.reshape(np.asarray(score),[-1,6])
			res = sess.run([bot.thrusters], {bot.input_nn: nn_input, bot.score: score})
			# res = sess.run([bot.thrusters, bot.train_step], {bot.input_nn: nn_input, bot.score: score})
			thrust = res[0][0]
			i = np.argmax(thrust)
			# print i
			if i==0:
				fx = -0.5
			elif i==2:
				fx = 0.5
			elif i==3:
				fy = -0.5
			elif i==5:
				fy = 0.5
			# print bot.x, bot.y
			# bot.add_fx(res[0][0][0])
			# bot.add_fy(res[0][0][1])
			
		else:
			fx = random.random()-0.5
			fy = random.random()-0.5

		bot.animate()
		freq = 1000
		if frame%freq == 0:
			pass
			# canvas.postscript(file="frames/frame_"+str(frame/freq)+".ps", colormode='color')
		frame = frame + 1
		# print fx,fy
		bot.add_fx(fx)
		bot.add_fy(fy)

		if bot.collisions > 0:
			import pdb
			score = [0, 0, 0, 0, 0, 0]
			if nn_input[0][0]*bot.velx > 0:
				score[1] = 10
			if nn_input[0][1]*bot.vely > 0:
				score[4] = 10
			if nn_input[0][0]*bot.velx < 0 and bot.velx < 0:
				score[0] = 50
			if nn_input[0][0]*bot.velx < 0 and bot.velx > 0:
				score[2] = 50
			if nn_input[0][1]*bot.vely < 0 and bot.vely < 0:
				score[3] = 50
			if nn_input[0][1]*bot.vely < 0 and bot.vely > 0:
				score[5] = 50
			# print score
			i=np.argmax(score)
			score = np.reshape(np.asarray(score),[-1,6])
			res = sess.run([bot.thrusters, bot.train_step, bot.loss, bot.input_nn], {bot.input_nn: nn_input, bot.score: score})
			
			# bot.add_fx(res[0][0][0])
			# bot.add_fy(res[0][0][1])
			# print 'r', bot.name, bot.collisions, res[0][0], res[2], i
			bot.reset_collisions()
		if bot.scale < 90:
			bot.scale = bot.scale+0.01
		if bot.health < 0:
			sbots = sorted(bots, key=lambda x: x.health, reverse=True)
			print "Combining bots %s and %s to bot %s"%(sbots[0].name, sbots[1].name, bot.name)
			bot.assign_avg_nn(sbots[0].nnet,sbots[1].nnet, sess)
			bot.health = sbots[0].health/2 + sbots[1].health/2 + random.random()*20
			# s_bots = bots.
			# bot.canvas.delete(bot.character)
	print bot_healths
	if restart:
		canvas.after(1, animator,bots)
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
bottom = Frame(root)
bottom.pack(side=BOTTOM, fill=BOTH, expand=True)
# f = Frame(root, height=400, width=400)
# f.pack_propagate(0)
# f.pack()
canvas = Canvas(root, width=1280, height = 720)
# f = Frame(root, height=30, width=400)
# f.pack_propagate(0)
# f.pack()
canvas.pack()
import random
bots = []
print 'Setting up'
colors = ['#f00','#0f0','#00f','#ff0','#f0f','#0ff','#fff','#000','#800','#080','#008','#880','#808','#088','#888']
from functools import partial
def delete_bot(bot):
	canvas.delete(bot.character)
	bots.remove(bot)
for i in xrange(15):
	bot = Bot(50+(i%2)*100 + i/5*200, (i%5)*90, 20, 1, canvas, str(i), color=colors[i])
	action_with_arg = partial(delete_bot,bot)
	b = Button(bottom, text="OK", command=action_with_arg, bg=colors[i])
	b.grid(row=0,column=i)
	bot.add_fx(0.1)
	bot.add_fy(0.1)
	bot.setup_nn()
	bots.append(bot)
print 'Setting up done'

sess.run(tf.initialize_all_variables())
train_writer = tf.train.SummaryWriter('./train', sess.graph)
animator(bots)
# canvas.after(100, test, bots)
root.mainloop()