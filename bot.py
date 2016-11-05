from physics import Physics
import math
import tensorflow as tf
import pygame
import numpy as np

class Bot(Physics):
	def __init__(self, x, y, radius, scale, screen, name='1', color='blue', health = 100.0):
		super(Bot,self).__init__(scale, x, y)
		self.screen = screen
		self.character = pygame.transform.scale(pygame.image.load("utils/animat1.png"), (radius*2, radius*2))
		self.rect = self.character.get_rect()
		self.radius = radius
		self.name = name
		self.collisions = 0
		self.health = health

	def move(self):
		old_pos = self.get_pos()
		width, height = self.screen.get_size()
		# print width, height, old_pos[0], old_pos[1]
		if old_pos[0]+self.radius > width and self.velx > 0:
			self.collide(0)
		if old_pos[0]-self.radius < 0 and self.velx < 0:
			self.collide(0)
		if old_pos[1]+self.radius > height and self.vely > 0:
			self.collide(90)
		if old_pos[1]-self.radius < 0 and self.vely < 0:
			self.collide(-90)

		new_pos = Physics.move(self)


		# print self.speed(), self.rect.left, self.rect.right, self.rect.top, self.rect.bottom, ((self.rect.right + self.rect.left)/2)/(old_pos[0]/5)
		self.rect.center=self.get_pos()
		
		self.screen.blit(self.character, self.rect)

		self.health = self.health - 0.01

	def speed(self):
		return self.velx, self.vely
		

	def collide(self, arg, obj=None):
		super(Bot, self).collide(arg, obj)
		self.collisions = self.collisions + 1
		self.health = self.health - 1
		if obj is not None:
			obj.health = obj.health - 1

	def surroundings(self, bots):
		surr = {'l':0, 'r':0, 'u':0, 'd':0}
		width, height = self.screen.get_size()
		for bot in bots:
			if bot == self:
				continue
			if bot.x < self.x:
				surr['l'] = surr['l']+(((bot.x-self.x)**2) + ((bot.y-self.y)**2))/(2*(width**2))
			else:
				surr['r'] = surr['r']+(((bot.x-self.x)**2) + ((bot.y-self.y)**2))/(2*(width**2))
			if bot.y < self.y:
				surr['u'] = surr['u']+(((bot.x-self.x)**2) + ((bot.y-self.y)**2))/(2*(height**2))
			else:
				surr['d'] = surr['d']+(((bot.x-self.x)**2) + ((bot.y-self.y)**2))/(2*(height**2))
		threshold = 20
		if True:
		# if self.x > 400-threshold:
			surr['r'] = surr['r']+(self.x)/width
		# if self.x < threshold:
			surr['l'] = surr['l']+(width-self.x)/width
		# if self.y > 400-threshold:
			surr['d'] = surr['d']+(self.y)/height
		# if self.y < threshold:
			surr['u'] = surr['u']+(height-self.y)/height
		return surr

	def collision_detect(self, obj):
		if (self.x - obj.x)**2 + (self.y - obj.y)**2 < (self.radius + obj.radius)**2:
			rvx = obj.x - self.x
			rvy = obj.y - self.y
			angle = math.atan2(rvy, rvx)
			# print math.degrees(angle), self.name, self.x, self.y, obj.name, obj.x, obj.y, (self.x - obj.x)**2 + (self.y - obj.y)**2
			self.collide(math.degrees(angle),obj)
			# obj.collide(math.degrees(angle))
			# print angle
			return True
		else:
			return False

	def reset_collisions(self):
		self.collisions = 0

	def animate(self):
		self.move()
		# self.screen.after(1000/60, self.animate)

	def assign_avg_nn(self, nnet1, nnet2, session):
		for k in self.nnet.keys():
			if isinstance(self.nnet[k], tf.Variable):
				session.run(self.nnet[k].assign(nnet1[k].eval(session=session)/2+nnet2[k].eval(session=session)/2))

	def setup_nn(self):
		input_size = 9
		layers = [10]
		output_size = 6
		self.nnet = {}
		with tf.variable_scope('bot_'+self.name):
			input = tf.placeholder(tf.float32, shape=[None,input_size], name="input")
			self.nnet['input'] = input
			score = tf.placeholder(tf.float32,shape=[None,output_size], name="score")
			self.nnet['score'] = score
			prev_input = input
			for i, size in enumerate(layers):
				w = tf.Variable(tf.random_uniform([input_size,size]), name="hidden_w_"+str(i))
				self.nnet["hidden_w_"+str(i)] = w
				b = tf.Variable(tf.random_uniform([size]), name="hidden_b_"+str(i))
				self.nnet["hidden_b_"+str(i)] = b
				output = tf.sigmoid(tf.matmul(prev_input,w)+b)
				self.nnet["output_"+str(i)] = output
				prev_input = output
				input_size = size
			
			ws = tf.Variable(tf.zeros([input_size,output_size]))
			self.nnet["hidden_ws"] = ws
			bs = tf.Variable(tf.zeros([output_size]))
			self.nnet["hidden_bs"] = bs
			pred = tf.nn.softmax(tf.matmul(output,ws)+bs)
			self.nnet["output_pred"] = pred
			optimizer = tf.train.AdagradOptimizer(0.1)

			loss_m = tf.reduce_mean(-tf.reduce_sum(score * tf.log(tf.maximum(pred,pred + 1e-10)), reduction_indices=[1]))
			train_step = optimizer.minimize(loss_m)

			self.op1 = output
			self.thrusters = pred
			self.train_step = train_step
			self.loss = loss_m
			self.input_nn = input
			self.score = score
			self.final = pred