import time
import math

class Physics(object):
	def __init__(self, scale, x, y, mass=5):
		self.scale = scale
		self.fx = 0.0
		self.fy = 0.0
		self.x = x
		self.y = y
		self.velx = 0.0
		self.vely = 0.0
		self.last_moved = time.time()
		self.last_collision_check = time.time()
		self.mass=mass

	def reset_time(self):
		self.last_moved = time.time()

	def get_time(self):
		td = time.time()-self.last_moved
		self.last_moved = time.time()
		return 0.1*self.scale#float(td*self.scale)

	def move(self):
		t = self.get_time()
		# print self.name, self.x, self.y, self.velx, self.vely, self.fx, self.fy, 't:',t, self.fy*t
		new_x = self.x + self.velx*t + 0.5*t**2*self.fx
		new_y = self.y + self.vely*t + 0.5*t**2*self.fy
		self.x=new_x
		self.y=new_y

		self.velx = self.velx + self.fx*t
		self.vely = self.vely + self.fy*t

		# if abs(self.velx) > 2:
		# 	self.velx = 2*self.velx/(abs(self.velx))
		# if abs(self.vely) > 2:
		# 	self.vely = 2*self.vely/(abs(self.vely))

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

	def collide(self, angle, obj=None):
		if time.time()-self.last_collision_check < 0.1:
			# print 'Too soon'
			return
		import pdb
		mangle = math.radians(angle)
		mangle90 = math.radians(90-angle)
		angle = math.atan2(self.vely, self.velx) - mangle
		# angle_90 = math.radians(90-angle)
		# angle = math.atan2(self.vely, self.velx)
		# angle_180 = math.radians(180-math.degrees(angle))
		angle_deg = (math.degrees(mangle))%360
		nvelx = self.velx
		nvely = self.vely
		if obj is None:
			if angle_deg >= 0 and angle_deg < 90: #(0,90)
				nvelx = -self.velx*math.cos(mangle)# + self.vely*math.sin(angle)
			elif angle_deg >= 90 and angle_deg < 180: #(90,180)
				nvely = -self.vely*math.sin(mangle)# + self.velx*math.cos(angle)
			elif angle_deg >= 180 and angle_deg < 270 :#(-90,-180)
				nvelx = -self.velx*math.cos(mangle)# + self.vely*math.sin(angle)
			else: #(0,-90)
				nvely = self.vely*math.sin(mangle)# + self.velx*math.cos(angle)
			# if angle_deg == 0 : pdb.set_trace()
		else:
			t = self.get_time()
			self.velx = self.velx - self.fx*t
			self.vely = self.vely - self.fy*t

			t = obj.get_time()
			obj.velx = obj.velx - obj.fx*t
			obj.vely = obj.vely - obj.fy*t

			nvelx = self.velx*(self.mass-obj.mass) + 2*obj.mass*obj.velx
			nvely = self.vely*(self.mass-obj.mass) + 2*obj.mass*obj.vely

			nvelx1 = obj.velx*(obj.mass-self.mass) + 2*self.mass*self.velx
			nvely1 = obj.vely*(obj.mass-self.mass) + 2*self.mass*self.vely

			# if not (self.velx*obj.velx < 0 or self.vely*obj.vely < 0 or (self.x/obj.x < obj.velx/self.velx or self.y/obj.y < obj.vely/self.vely )):
			# 	return

			ovel = (self.velx**2 + self.vely**2)**0.5
			ovel2 = (obj.velx**2 + obj.vely**2)**0.5

			angle2 = math.atan2(obj.vely, obj.velx) - mangle
			
			nvel = (ovel*math.cos(angle)*(self.mass-obj.mass) + 2*obj.mass*ovel2*math.cos(angle2))/(self.mass+obj.mass)
			nvelx = nvel*math.cos(mangle) - ovel*math.sin(angle)*math.cos(mangle+math.radians(90))/(self.mass+obj.mass)
			nvely = nvel*math.sin(mangle) + ovel*math.sin(angle)*math.sin(mangle+math.radians(90))/(self.mass+obj.mass)
			nvel2 = (ovel2*math.cos(angle)*(obj.mass-self.mass) + 2*self.mass*ovel*math.cos(angle))/(obj.mass+self.mass)
			nvelx2 = nvel2*math.cos(mangle) + ovel2*math.sin(angle2)*math.cos(mangle+math.radians(90))/(self.mass+obj.mass)
			nvely2 = nvel2*math.sin(mangle) + ovel2*math.sin(angle2)*math.sin(mangle+math.radians(90))/(self.mass+obj.mass)
			# pdb.set_trace()

			obj.velx = nvelx2
			obj.vely = nvely2


			# xDist = self.x - obj.x
			# yDist = self.y - obj.y
			# distSquared = xDist*xDist + yDist*yDist
			# #Check the squared distances instead of the the distances, same result, but avoids a square root.
			# if(distSquared <= (self.radius + obj.radius)*(self.radius + obj.radius)):
			# 	velxocity = obj.velx - self.velx
			# 	velyocity = obj.vely - self.vely
			# 	dotProduct = xDist*velxocity + yDist*velyocity
			# 	#Neat vector maths, used for checking if the objects moves towards one another.
			# 	if(dotProduct > 0):
			# 		collisionScale = dotProduct / distSquared
			# 		xCollision = xDist * collisionScale
			# 		yCollision = yDist * collisionScale
			# 		#The Collision vector is the speed difference projected on the Dist vector,
			# 		#thus it is the component of the speed difference needed for the collision.
			# 		combinedMass = self.mass + obj.mass
			# 		collisionWeightself = 2 * obj.mass / combinedMass
			# 		collisionWeightobj = 2 * self.mass / combinedMass
			# 		self.velx += collisionWeightself * xCollision
			# 		self.vely += collisionWeightself * yCollision
			# 		obj.velx -= collisionWeightobj * xCollision
			# 		obj.vely -= collisionWeightobj * yCollision
   #              
   #          


		# nvelx = -(abs(self.velx)*math.cos(angle))# - self.vely*math.cos(angle))
		# nvely = -(abs(self.vely)*math.sin(angle))# + self.velx*math.cos(angle))

		self.velx = nvelx
		self.vely = nvely
		# print 'collide',self.name, angle_deg, math.degrees(mangle), self.velx, self.vely, obj
		self.last_collision_check = time.time()
		# if angle_deg%90==0:
		# 	1/0

	def get_pos(self):
		return self.x, self.y