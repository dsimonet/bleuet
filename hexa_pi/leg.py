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

		self.name = "leg" + str(len(LegSmooth._registry))

		# Instanciate motor class for each par of leg
		self.mot_phi = Motor(_phi)
		self.mot_A = Motor(_A)
		self.mot_B = Motor(_B)

		self.mot_B.reverseMotor()

		self.side_Phi = True
		self.side_A = True
		self.side_B = True
		

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


	@staticmethod
	def setSpeedAll(value):
		for leg in LegSmooth:
			leg.setSpeed(value)

	@staticmethod
	def allOff() :
		for leg in LegSmooth :
			leg.off()


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

		#assign new goal value 
		self.phiTo = _phi
		self.aTo = _a
		self.bTo = _b


		if self.ready() :
			#if we are ready we can go for a trip from where we are
			#so position and time are reseted and are our new starting point

			self.timeBegin = time.time()

			self.phiFrom = self.phiValue
			self.aFrom = self.aValue
			self.bFrom = self.bValue
			
			#looking for the longest distance we have to travel on each 3 motor. It's our duration for all 3 motors
			# This is because all motor for each leg is sync. 
			maxDuration = max( [abs(self.phiTo - self.phiFrom), abs(self.aTo - self.aFrom), abs(self.bTo - self.bFrom)] );
			self.duration = float ( maxDuration ) / self.speed 

		else:
			# else it's a bit triky. 
			# we find the longest distance between *actual* position and to the new distance (it the trip we have to do)
			distList = [abs(self.phiTo - self.phiValue), abs(self.aTo - self.aValue), abs(self.bTo - self.bValue)]
			# and our new duration is the time we already done (cause we can't get it back), and duration between actual position and the new position
			self.duration = time.time()-self.timeBegin + float ( max(distList) / self.speed ) 



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


	def isSoftLimiteActive(self, _v):
		pass

	def setLimits(self, _minPhi, _maxPhi, _minA, _maxA, _minB, _maxB) : 
		pass



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

	LegSmooth.setSpeedAll(20)

	for leg in LegSmooth :
		leg.position(0,0,0)

	while not LegSmooth.allReady() :
		LegSmooth.updateAll()

	try :
		while True :
			if LegSmooth.allReady() :
				for leg in LegSmooth :
					leg.position(random.randint(-30,30),random.randint(-90,90),random.randint(-90,90))
				LegSmooth.positionSync()

			LegSmooth.updateAll()

	except KeyboardInterrupt:

		for leg in LegSmooth :
			leg.position(0,0,0)

		while not LegSmooth.allReady() :
			LegSmooth.updateAll()

		time.sleep(0.1)

		LegSmooth.allOff()

		time.sleep(0.1)

