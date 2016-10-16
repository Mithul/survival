from physics import Physics
import math
import tensorflow as tf

class Bot(Physics):
	def __init__(self, x, y, radius, scale, canvas, name='1'):
		super(Bot,self).__init__(scale, x, y)
		self.canvas = canvas
		self.character = self.canvas.create_oval(x-radius, y-radius, x+radius, y+radius, outline='white', fill='blue')
		self.canvas.pack()
		self.radius = radius
		self.name = name
		self.collisions = 0
		self.health = 100

	def move(self):
		old_pos = self.get_pos()

		if old_pos[0] > 400:
			self.collide(0)
		if old_pos[0] < 0:
			self.collide(0)
		if old_pos[1] > 400:
			self.collide(90)
		if old_pos[1] < 0:
			self.collide(-90)

		new_pos = Physics.move(self)
		self.canvas.move(self.character, new_pos[0] - old_pos[0], new_pos[1] - old_pos[1])
		self.canvas.update()
		import pdb
		# pdb.set_trace()

	def collide(self, arg, obj=None):
		super(Bot, self).collide(arg, obj)
		self.collisions = self.collisions + 1

	def surroundings(self, bots):
		surr = {'l':0, 'r':0, 'u':0, 'd':0}
		for bot in bots:
			if bot == self:
				continue
			if bot.x < self.x:
				surr['l'] = surr['l']+1
			else:
				surr['r'] = surr['r']+1
			if bot.y < self.y:
				surr['u'] = surr['u']+1
			else:
				surr['d'] = surr['d']+1
		threshold = 20
		if True:
		# if self.x > 400-threshold:
			surr['r'] = surr['r']+(self.x)/400
		# if self.x < threshold:
			surr['l'] = surr['l']+(400-self.x)/400
		# if self.y > 400-threshold:
			surr['d'] = surr['d']+(self.y)/400
		# if self.y < threshold:
			surr['u'] = surr['u']+(400-self.y)/400
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
		with tf.variable_scope('bot_'+self.name):
			input = tf.placeholder(tf.float32, shape=[None,input_size], name="input")
			score = tf.placeholder(tf.float32,shape=[None,2], name="score")
			w1 = tf.Variable(tf.random_normal([input_size,5]))
			b1 = tf.Variable(tf.random_normal([5]))
			op1 = tf.tanh(tf.matmul(input,w1)+b1)
			w2 = tf.Variable(tf.random_normal([5,2]))
			b2 = tf.Variable(tf.random_normal([2]))
			op2 = tf.tanh(tf.matmul(op1,w2)+b2)
			w3 = tf.Variable(tf.zeros([2,1]))
			b3 = tf.Variable(tf.zeros([1]))
			pred = tf.tanh(tf.matmul(op2,w3)+b3)
			optimizer = tf.train.GradientDescentOptimizer(0.1)
			loss_m = -tf.reduce_sum(op2-score)
			train_step = optimizer.minimize(loss_m)

			self.op1 = op1
			self.thrusters = op2
			self.train_step = train_step
			self.loss = loss_m
			self.input_nn = input
			self.score = score
			self.final = pred