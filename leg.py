#!/usr/bin/env python
#-*- coding: utf-8 -*-


#Dsimonet

#from __future__ import division
#from threading import Thread
#import ease
from motor import motor

#see here https://stackoverflow.com/questions/739882/iterating-over-object-instances-of-a-given-class-in-python
class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)


class Leg() :

	# for iterate over instances
	__metaclass__ = IterRegistry
	_registry = []

	#_counter = 0
	#_duration = 64

	def __init__(self, _phi, _A, _B):

		#register and iteration
		self._registry.append(self)
		self.name = "Leg_" + str(len(self._registry)-1)

		self.side = True #True =  "normal" & False = "reverse"

		# Instanciate motor class for each par of leg
		self.mot_phi = motor(_phi)
		self.mot_A = motor(_A)
		self.mot_B = motor(_B)

		self.mot_A.reverseMotor()
		

	#METHODES STATICS

	@staticmethod
	def allPosition(_phi, _a, _b):
		for leg in Leg._registry :
			leg.position(_phi, _a, _b)

	

	#METHODES

	def isReady() :
		return self.ready

	def position(self, _phi, _A, _B):
		self.mot_phi.move(_phi)
		self.mot_A.move(_A)
		self.mot_B.move(_B)

	def reverseLeg(self):
		self.mot_phi.reverseMotor()
		self.mot_A.reverseMotor()
		self.mot_B.reverseMotor()
		self.side = not self.side

	def height(self, _v):
		self.mot_A.move(50-_v/2)
		self.mot_B.move(_v/2)

	def orient(self, _phi):
		self.mot_phi.move(_phi)

	def off(self):
		self.mot_phi.off()
		self.mot_A.off()
		self.mot_B.off()

	def moveTo(self, position) :
		if position == "stand":
			self.mot_phi.move(0)
			self.mot_A.move(40)
			self.mot_B.move(20)		
			return

		if position == "unfold":
			self.mot_phi.move(0)
			self.mot_A.move(0)
			self.mot_B.move(0)

		if position == "fold":
			self.mot_phi.move(0)
			self.mot_A.move(0)
			self.mot_B.move(0)	

	"""



	#veleurs des positions des moteurs 
	# 50 5 et 70 pour un stand
	self.phi = 50
	self.a = 5
	self.b = 70

	self.phiFrom = self.phi
	self.aFrom = self.a
	self.bFrom = self.b

	self.phiTo = self.phi
	self.aTo = self.a
	self.bTo = self.b 
		
	@staticmethod
	def speed(v):
		Leg._duration = v

	@staticmethod
	def allReady() :
		for i in Leg._registry :
			if i.ready :
				continue
			else:
				return False
		return True


	@staticmethod
	def waitUntilFinish():
		while not Leg.allReady() :
			pass
	

	def updateSoft(self):

		#on calcul la position actuel avec une fonction ease
		#ease(t, b, c, d)
		# t is the current time (or position) of the tween.
		# b is the beginning value of the property.
		# c is the change between the beginning and destination value of the property.
		# d is the total time of the tween.
		self.phi = ease.easeInOutQuad(float(self._counter), self.phiFrom, self.phiTo-self.phiFrom, float(self._duration) )
		self.a = ease.easeInOutQuad(float(self._counter), self.aFrom, self.aTo-self.aFrom, float(self._duration) )
		self.b = ease.easeInOutQuad(float(self._counter), self.bFrom, self.bTo-self.bFrom, float(self._duration) )

		# on update le counter qui nous laisse une trace de notre position sur la courbe de ease

		if self._counter < self._duration :
			self._counter += 1
			self.ready = False
		else:
			self.ready = True

		#On fait bouger les moteurs en fonction des nouvelles valeurs calculé
		self.move(self.phi, self.a, self.b)
	
"""



#excuted if this doc is not imported
# for testing purpose only
if __name__ == '__main__':

	import time

	#Create leg for robot and passing them were are connected motor
	leg_0 = Leg(0,1,2)
	leg_1 = Leg(4,5,6)
	leg_2 = Leg(8,9,10)


	for a in range(0,5):

		for leg in Leg :
			leg.height(100)
			leg.moveTo("unfold")

		leg_0.orient(-10)
		leg_1.orient(30)
		leg_2.orient(-10)

		time.sleep(0.5)

		for leg in Leg :
			leg.height(10)

		time.sleep(0.5)

		leg_0.orient(10)
		leg_1.orient(-10)
		leg_2.orient(30)

		time.sleep(0.5)

	"""
	for a in range(0,10):
		for i in range(0,100):
			for leg in Leg :
				leg.height(0, i)

	"""
	for i in Leg :
		i.mot_phi.off()
		i.mot_A.off()
		i.mot_B.off()
