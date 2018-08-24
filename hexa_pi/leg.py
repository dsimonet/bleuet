#!/usr/bin/env python
#-*- coding: utf-8 -*-


#Dsimonet

#from __future__ import division

from motor import *

#see here https://stackoverflow.com/questions/739882/iterating-over-object-instances-of-a-given-class-in-python
class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)


class Leg() :

	# for iterate over instances
	__metaclass__ = IterRegistry
	_registry = []

	def __init__(self, _phi, _A, _B):

		#register and iteration
		Leg._registry.append(self)
		self.name = "Leg_" + str(len(self._registry)-1)

		self.side = True #True =  "normal" & False = "reverse"

		# Instanciate motor class for each par of leg
		self.mot_phi = Motor(_phi)
		self.mot_A = Motor(_A)
		self.mot_B = Motor(_B)

		self.mot_A.reverseMotor()
		

	#METHODES STATICS

	@staticmethod
	def allPosition(_phi, _a, _b):
		for leg in Leg._registry :
			leg.position(_phi, _a, _b)

	

	#METHODES

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

