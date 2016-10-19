from physics import Physics
import math
import tensorflow as tf

class Bot(Physics):
	def __init__(self, x, y, radius, scale, canvas, name='1', color='blue', health = 100.0):
		super(Bot,self).__init__(scale, x, y)
		self.canvas = canvas
		self.character = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline='white', fill=color)
		self.canvas.pack()
		self.radius = radius
		self.name = name
		self.collisions = 0
		self.health = health

	def move(self):
		old_pos = self.get_pos()

		if old_pos[0] > self.canvas.winfo_width() and self.velx > 0:
			self.collide(0)
		if old_pos[0] < 0 and self.velx < 0:
			self.collide(0)
		if old_pos[1] > self.canvas.winfo_height() and self.vely > 0:
			self.collide(90)
		if old_pos[1] < 0 and self.vely < 0:
			self.collide(-90)

		new_pos = Physics.move(self)
		self.canvas.move(self.character, new_pos[0] - old_pos[0], new_pos[1] - old_pos[1])
		self.canvas.update()
		self.health = self.health - 0.01
		if self.health < 0:
			self.canvas.delete(self.character)

	def collide(self, arg, obj=None):
		super(Bot, self).collide(arg, obj)
		self.collisions = self.collisions + 1
		self.health = self.health - 1
		if obj is not None:
			obj.health = obj.health - 1

	def surroundings(self, bots):
		surr = {'l':0, 'r':0, 'u':0, 'd':0}
		for bot in bots:
			if bot == self:
				continue
			if bot.x < self.x:
				surr['l'] = surr['l']+(((bot.x-self.x)**2) + ((bot.y-self.y)**2))/(2*(self.canvas.winfo_width()**2))
			else:
				surr['r'] = surr['r']+(((bot.x-self.x)**2) + ((bot.y-self.y)**2))/(2*(self.canvas.winfo_width()**2))
			if bot.y < self.y:
				surr['u'] = surr['u']+(((bot.x-self.x)**2) + ((bot.y-self.y)**2))/(2*(self.canvas.winfo_height()**2))
			else:
				surr['d'] = surr['d']+(((bot.x-self.x)**2) + ((bot.y-self.y)**2))/(2*(self.canvas.winfo_height()**2))
		threshold = 20
		if True:
		# if self.x > 400-threshold:
			surr['r'] = surr['r']+(self.x)/self.canvas.winfo_width()
		# if self.x < threshold:
			surr['l'] = surr['l']+(self.canvas.winfo_width()-self.x)/self.canvas.winfo_width()
		# if self.y > 400-threshold:
			surr['d'] = surr['d']+(self.y)/self.canvas.winfo_height()
		# if self.y < threshold:
			surr['u'] = surr['u']+(self.canvas.winfo_height()-self.y)/self.canvas.winfo_height()
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
		# self.canvas.after(1000/60, self.animate)

	def setup_nn(self):
		input_size = 9
		layers = [8,8,8,8,8]
		output_size = 6
		with tf.variable_scope('bot_'+self.name):
			input = tf.placeholder(tf.float32, shape=[None,input_size], name="input")
			score = tf.placeholder(tf.float32,shape=[None,output_size], name="score")
			prev_input = input
			for i, size in enumerate(layers):
				w = tf.Variable(tf.random_uniform([input_size,size]), name="hidden_"+str(i))
				b = tf.Variable(tf.random_uniform([size]), name="hidden_"+str(i))
				output = tf.sigmoid(tf.matmul(prev_input,w)+b)
				prev_input = output
				input_size = size
			
			ws = tf.Variable(tf.zeros([input_size,output_size]))
			bs = tf.Variable(tf.zeros([output_size]))
			pred = tf.nn.softmax(tf.matmul(output,ws)+bs)
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