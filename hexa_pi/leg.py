#!/usr/bin/env python
#-*- coding: utf-8 -*-


#Dsimonet

#from __future__ import division

from motor import *

#see here https://stackoverflow.com/questions/739882/iterating-over-object-instances-of-a-given-class-in-python
class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

######################
"""	LEG """
######################

class Leg() :

	# for iterate over instances
	__metaclass__ = IterRegistry
	_registry = []

	def __init__(self, _phi, _A, _B):

		#register and iteration
		Leg._registry.append(self)

		self.side = True
		self.name = "leg" + str(len(LegSmooth._registry))

		# Instanciate motor class for each par of leg
		self.mot_phi = Motor(_phi)
		self.mot_A = Motor(_A)
		self.mot_B = Motor(_B)

		#self.mot_B.reverseMotor()
		

	#METHODES STATICS

	@staticmethod
	def allPosition(_phi, _a, _b):
		for leg in Leg._registry :
			leg.position(_phi, _a, _b)

	@staticmethod
	def allSetSide(_v):
		for leg in Leg._registry :
			leg.setSide(_v)
	
	#METHODES

	def position(self, _phi, _A, _B):
		self.mot_phi.move(_phi)
		self.mot_A.move(_A)
		self.mot_B.move(_B)

	def setSide(self, _v):

		if _v == True or _v == False :
			if not _v == self.side :
				self.mot_A.setSide(_v)
				self.mot_B.setSide(_v)
				self.side = _v

	def height(self, _v):
		self.mot_A.move(50-_v/2)
		self.mot_B.move(_v/2)

	def orient(self, _phi):
		self.mot_phi.move(_phi)

	def off(self):
		self.mot_phi.off()
		self.mot_A.off()
		self.mot_B.off()


######################
"""	LEG SMOOTH """
######################


"""
Increasing Speed should augment velocity or reduce time beetween the start and the arrive of position
We have to keep trace of the last update. Like this mouvement will be calcultate over time/distance = speed and not just called where ever it want



"""



import ease
import time
import math

class LegSmooth(Leg) :

	"""
	even if it seems to be  useless to use this class to pilote fast motor (ex with speed >= 450)
	with this class a small movement (short distance) will be synchronized with
	long movement (long distance) over the different parts of the leg.
	this could be useful for nice and graceful movement 
	short story --> all parts of the leg will arrive at the goal position at the same time and
	synchronized no matter distance traveled. All synchronized on the maximum time obviously
	"""


	lastLegUpdated = 0

	def __init__(self, _phi, _a, _b):

		#init inherited class
		Leg.__init__(self, _phi, _a, _b)

		#values
		self.speed = float(250)#mm/s or degres/s --> 9G servo is 0.12second/ 60degree = 500 °/S
		self.duration = 0
		self.timeBegin = 0

		self.phiValue = 0.0
		self.aValue = 0.0
		self.bValue = 0.0

		self.phiFrom = 0.0
		self.aFrom = 0.0
		self.bFrom = 0.0

		self.phiTo = 0.0
		self.aTo = 0.0
		self.bTo = 0.0

		#Constant

		self.position(0,0,0)

	#METHODES STATICS

	@staticmethod
	def updateAll():
		for leg in LegSmooth:
			leg.update()

	@staticmethod
	def updateNextLeg():
		legToUpdate = (LegSmooth.lastLegUpdated+1)%len(LegSmooth._registry)
		LegSmooth._registry[ legToUpdate ].update()
		LegSmooth.lastLegUpdated += 1

	@staticmethod
	def allReady():
		for leg in LegSmooth:
			if not leg.ready() :
				return False
		return True

	@staticmethod
	def setAllSpeed(_v):
		while(not LegSmooth.allReady) :
			pass
		for leg in LegSmooth:
			leg.setSpeed(_v)

	@staticmethod
	def positionSync():
		"""
		To sync arrived time. We simply look for the longest duration of all leg and apply it to all leg
		"""

		distList = []

		for leg in LegSmooth:
			distList.append( leg.duration )
		for leg in LegSmooth :
			leg.duration = max(distList)


	#METHODES

	def setSpeed(self, value):
		"""
		no matter whater what you think, but float() cast avoid spicy bug
		"""
		if not value == 0:
			self.speed = float(value)

	def position(self, _phi, _a, _b):
		"""
		Set position of the leg by giving it 3 values
		"""

		if self.ready() :

			self.phiFrom = self.phiValue
			self.aFrom = self.aValue
			self.bFrom = self.bValue

			self.timeBegin = time.time()

		else :
			prevDone = time.time()-self.timeBegin
			prevDuration = self.duration
			pass#self.duration -= (time.time()-self.timeBegin)


		self.phiTo = _phi
		self.aTo = _a
		self.bTo = _b


		#looking for distance max --> this move will be the longest and need to syncronyse
		distList = [abs(self.phiTo - self.phiFrom), abs(self.aTo - self.aFrom), abs(self.bTo - self.bFrom)]
		self.duration = float ( max(distList) / self.speed ) 


	def update(self):
		"""
		compute position from last position trough a ease function
		ease(t, b, c, d)
		t is the current time (or position) of the tween.
		b is the beginning value of the property.
		c is the change between the beginning and destination value of the property.
		d is the total time of the tween.
		"""
		
		if (time.time()-self.timeBegin) < self.duration :
			self.phiValue = ease.easeInOutQuad(time.time()-self.timeBegin, self.phiFrom, self.phiTo-self.phiFrom, self.duration) 
			self.aValue = ease.easeInOutQuad(time.time()-self.timeBegin, self.aFrom, self.aTo-self.aFrom, self.duration) 
			self.bValue = ease.easeInOutQuad(time.time()-self.timeBegin, self.bFrom, self.bTo-self.bFrom, self.duration)
		else : 
			self.phiValue = self.phiTo
			self.aValue = self.aTo
			self.bValue = self.bTo


		#Moving motor with inherited methode to the computed value
		Leg.position(self, self.phiValue, self.aValue, self.bValue)



	def ready(self):
		if (time.time()-self.timeBegin) < self.duration :
			return False
		else:
			return True



######################
"""	LEG IK """
######################

# size in mm and angle in degrees or radian

#			^  0°
#	-x+y	|		+x+y
#			|
#			| XY origin
#  90° -----R--------> 270°
#			|
#	-x-y	|		-y+x
#			|
#		   180°


import math

class LegIK (LegSmooth):

	robotReverse = 1 #1 for normal side and -1 for reverse

	def __init__(self, _phi, _A, _B, _orient=0):
		LegSmooth.__init__(self, _phi, _A, _B)

		#chain of parent to child is robot -> Coxa -> Femur -> tibia

		#idea is to orient to coxa in direction of the goal
		# and to solve in 2D angle of coxa to femur and femur to tibia to hit the goal

		#pos of leg from robot origin
		# and orientation from origin (front is 0°)
		self.orient = _orient
		self.posX = 0
		self.posY = 0

		self.minRot = -80
		self.maxRot = 80

		self.coxaZ = 11.15

		self.coxaLen = 28.70
		self.femurLen = 41.45
		self.tibiaLen = 47.639

	def SetOrient(self, degres):
		self.orient = degres%360

	def setPosition(self, _x, _y):
		self.posX = _x
		self.posY = _y

	def getSide(self):
		#side : 1 = left, -1 = right
		if self.orient < 180 :
			return 1
		else:
			return -1

	def position(self,_x,_y,_z):

		#computing Orientation of the leg
		#math.atan2(y, x) result -pi to pi 
		goalOrient = math.degrees(math.atan2(math.fabs(_y),math.fabs(_x)))
		goalOrientCorrected = self.orient - goalOrient
		#print "goalOrientCorrected",goalOrientCorrected


		#now have to resolve 2 angles of femur & coxa and tibia & femur 
		#but on the same plane.

		#calculate height for coxa from floor (corrected by side of the robot)
		heightCoxa = _z + self.coxaZ*LegIK.robotReverse
		#print "height goal", heightCoxa
		"""
		#calculate air (or floor) distance bettween heightCoxa and goal
		#it's position of robot&coxa axis  (2d) ---> distance (pythagore) minus coxa leng
		lengGoal = math.sqrt( (x-self.posX)*(x-self.posX)+(y-self.posY)*(y-self.posY) ) - self.coxaLen
		print "leng goal", lengGoal

		#calculate 2D distance beetween goal on the floor and axis point of femur& coxa
		distGoal = math.sqrt(  heightCoxa*heightCoxa+lengGoal*lengGoal ) 
		print "dist goal", distGoal

		# calculate angle beetween floor and distance ligne
		angleDistCoxaHeight = math.degrees(math.acos(heightCoxa/distGoal))
		print "angleDistCoxaHeight", angleDistCoxaHeight

		angleGoalFemur = math.degrees(math.acos( (self.tibiaLen*self.tibiaLen - self.femurLen*self.femurLen - distGoal*distGoal)/(-2*self.femurLen*distGoal) ))
		print "angleGoalFemur", angleGoalFemur

		angleFemureCoxa = 90 - (angleDistCoxaHeight + angleGoalFemur)
		print "angleFemureCoxa", angleFemureCoxa

		angleFemurTibia =  math.degrees(math.acos(  (distGoal*distGoal-self.tibiaLen*self.tibiaLen-self.femurLen*self.femurLen)/(-2*self.tibiaLen*self.femurLen) ))
		print "angleFemurTibia", angleFemurTibia

		correctedAngleFemurTibia = 90 - angleFemurTibia
		print "angleFemurTibia", angleFemurTibia
		"""
		LegSmooth.position(self, goalOrientCorrected,0,0)
		#print "------"
		return True




# excuted if this doc is not imported
# for testing purpose only
if __name__ == '__main__':

	import random

	leg_1 = LegSmooth(24,25,26)
	leg_2 = LegSmooth(20,21,22)
	leg_3 = LegSmooth(16,17,18)
	leg_4 = LegSmooth(8, 9, 10)
	leg_5 = LegSmooth(4, 5, 6)
	leg_6 = LegSmooth(0, 1, 2)

	LegSmooth.setAllSpeed(150)

	try :
		while True :
			if LegSmooth.allReady() :
				for leg in LegSmooth :
					leg.position(random.randint(-30,30),random.randint(-90,90),random.randint(-90,90))
				LegSmooth.positionSync()

			LegSmooth.updateAll()

	except KeyboardInterrupt:
		pass

