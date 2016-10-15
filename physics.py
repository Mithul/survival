import time
import math

class Physics(object):
	def __init__(self, scale, x, y):
		self.scale = scale
		self.fx = 0.0
		self.fy = 0.0
		self.x = x
		self.y = y
		self.velx = 0.0
		self.vely = 0.0
		self.last_moved = time.time()

	def reset_time(self):
		self.last_moved = time.time()

	def get_time(self):
		td = time.time()-self.last_moved
		self.last_moved = time.time()
		return float(td*self.scale)

	def move(self):
		t = self.get_time()
		print self.x, self.y, self.velx, self.vely, self.fx, self.fy, t, self.fy*t
		new_x = self.x + self.velx*t + 0.5*t**2*self.fx
		new_y = self.y + self.vely*t + 0.5*t**2*self.fy
		self.x=new_x
		self.y=new_y

		self.velx = self.velx + self.fx*t
		self.vely = self.vely + self.fy*t

		self.force_decay()

		return self.x, self.y

	def force_decay(self):
		self.fx = self.fx * 0.5
		self.fy = self.fy * 0.5
		if self.fx < 0.001:
			self.fx = 0.0
		if self.fy < 0.001:
			self.fy = 0.0

	def add_fx(self, fx):
		self.fx = self.fx + fx

	def add_fy(self, fy):
		self.fy = self.fy + fy

	def add_force(self, fx, fy):
		self.fx = self.fx + fx
		self.fy = self.fy + fy

	def collide(self, angle):
		angle = math.atan2(self.vely, self.velx) - math.radians(angle%90)
		# angle_90 = math.radians(90-angle)
		# angle = math.atan2(self.vely, self.velx)
		# angle_180 = math.radians(180-math.degrees(angle))
		angle_deg = math.degrees(angle)
		nvelx = self.velx
		nvely = self.vely
		if angle_deg >= 0 and angle_deg < 90:
			 nvelx = -self.velx
		elif angle_deg >= 90:
			 nvely = -self.vely
		elif angle_deg < -90 :
			 nvelx = -self.velx
		else: #angle_deg < -90:
			 nvely = -self.vely
		# nvelx = -(abs(self.velx)*math.cos(angle))# - self.vely*math.cos(angle))
		# nvely = -(abs(self.vely)*math.sin(angle))# + self.velx*math.cos(angle))

		self.velx = nvelx
		self.vely = nvely
		print math.degrees(angle), self.velx, self.vely

	def get_pos(self):
		return self.x, self.y