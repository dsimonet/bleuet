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


##############################################
# Leg
##############################################

class Leg() :

	# for iterate over instances
	__metaclass__ = IterRegistry
	_registry = []

	#_counter = 0
	#_duration = 64

	def __init__(self, _bus, _phi, _A, _B):

		#register and iteration
		self._registry.append(self)
		self.name = "Leg_" + str(len(self._registry)-1)

		self.ready = False

		#not used yet
		self.bus = _bus

		# les valeurs des moteurs sur la carte de pilotage
		self.mot_phi = motor(_phi)
		self.mot_A = motor(_A)
		self.mot_A.reverseMotor()
		self.mot_B = motor(_B)
		

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

		self.standPosition()

	#METHODES STATICS

	@staticmethod
	def updateAll() :
		for i in Leg._registry:
			i.update()

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

	@staticmethod
	def allPosition(_phi, _a, _b):
		for p in Leg._registry :
			p.position(_phi, _a, _b)

	#METHODES

	def isReady() :
		return self.ready

	def position(self, _phi, _A, _B):
		#on va update la nouvelle direction des moteurs
		#on stock la valeur actuel dans la position d'origine
		self.phiFrom = self.phi
		self.aFrom = self.a
		self.bFrom = self.b

		#les nouvelles valeurs ou on doit allé sont enregistré
		self.phiTo = _phi
		self.aTo = _A
		self.bTo = _B

		self._counter = 0
		self.ready = False


	def move(self, _phi, _a, _b):
		self.pwm.set_pwm(self.motorPhi, 1, self.servoPC(_phi) )
		self.pwm.set_pwm(self.motorA, 1, self.servoPC(_a) )
		self.pwm.set_pwm(self.motorB, 1, self.servoPC(_b) )

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
	
	def update(self):
		pass

	# POSITION

	def standPosition(self):
		self.mot_phi.move(0)
		self.mot_A.move(40)
		self.mot_B.move(20)




#excuted if this doc is not imported
if __name__ == '__main__':

	import time
	import random

	#Create leg for robot and passing them were are connected motor
	leg_0 = Leg(0,0,1,2)
	leg_1 = Leg(0,4,5,6)
	leg_2 = Leg(0,8,9,10)

	
	for j in range(0,50):
		for i in Leg :
			i.mot_A.move(50-j)
			i.mot_B.move(j)
		time.sleep(0.05)
	
	for j in range(0,50):
		for i in Leg :
			i.mot_A.move(50-j)
			i.mot_B.move(j)
		time.sleep(0.05)

	for i in Leg :
		i.standPosition()

	time.sleep(0.5)

	for i in Leg :
		i.mot_phi.off()
		i.mot_A.off()
		i.mot_B.off()
