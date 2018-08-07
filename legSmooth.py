#!/usr/bin/env python
#-*- coding: utf-8 -*-


import ease
import time
from leg import Leg
from intervallometre import *


class LegSmooth(Leg) :

	_duration = 16

	def __init__(self, _phi, _A, _B) :
		Leg.__init__(self, _phi, _A, _B)

		self._counter = LegSmooth._duration
		self.name = "Leg_"+ str(len(LegSmooth._registry)-1)
		#veleurs des positions des moteurs 
		# 50 5 et 70 pour un stand
		self.phi = 0
		self.a = 0
		self.b = 0

		self.phiFrom = self.phi
		self.aFrom = self.a
		self.bFrom = self.b

		self.phiTo = self.phi
		self.aTo = self.a
		self.bTo = self.b 	


	@staticmethod
	def startThread():
		LegSmooth._timer = Intervallometre(0.001, LegSmooth.updateSoftAll)
		LegSmooth._timer.setDaemon(True)
		LegSmooth._timer.start()
		time.sleep(0.1)

	@staticmethod
	def setSpeed(v):
		for leg in LegSmooth:
			leg.phiFrom = leg.phi
			leg.aFrom = leg.a
			leg.bFrom = leg.b

			leg.phiTo = leg.phi
			leg.aTo = leg.a
			leg.bTo = leg.b 	
			leg._counter = v

		LegSmooth._duration = v
	
	@staticmethod
	def closeThread():
		LegSmooth._timer.stop()

	@staticmethod
	def offAllLegSmooth():
		for leg in LegSmooth :
			leg.off()
		time.sleep(0.1)

	@staticmethod
	def waitUntilFinish():
		if LegSmooth._duration > 1 :
			while 1 :
				if LegSmooth.allReady() :
					break
				else:
					time.sleep(0.03)
		else:
			time.sleep(0.1)
			
	@staticmethod
	def allReady():
		for leg in LegSmooth :
			if leg.ready() :
				pass
			else:
				return False
		return True

	@staticmethod
	def updateSoftAll():
		for leg in LegSmooth:
			leg.updateSoft()

	def ready(self):
		if self._counter == LegSmooth._duration :
			return True
		else:
			return False
	

	def position(self, _phi, _A, _B):

		#stock current position in from value
		self.phiFrom = self.phi
		self.aFrom = self.a
		self.bFrom = self.b

		#stock new position in to value
		self.phiTo = _phi
		self.aTo = _A
		self.bTo = _B

		if(LegSmooth._duration > 1):
			self._counter = 0

	def orient(self, _phi):
		self.position(_phi, self.aTo, self.bTo)

	def grab(self, _A, _B):
		self.position(self.phiTo, _A, _B)

	def updateSoft(self):

		if(LegSmooth._duration > 1):
			#compute position from last position trough a ease function
			#ease(t, b, c, d)
			# t is the current time (or position) of the tween.
			# b is the beginning value of the property.
			# c is the change between the beginning and destination value of the property.
			# d is the total time of the tween.
			self.phi = ease.easeInOutQuad(float(self._counter), self.phiFrom, self.phiTo-self.phiFrom, float(LegSmooth._duration) )
			self.a = ease.easeInOutQuad(float(self._counter), self.aFrom, self.aTo-self.aFrom, float(LegSmooth._duration) )
			self.b = ease.easeInOutQuad(float(self._counter), self.bFrom, self.bTo-self.bFrom, float(LegSmooth._duration) )

			if self._counter < LegSmooth._duration :
				self._counter += 1

			#Moving motor with inherited methode to the computed value
			Leg.position(self, self.phi, self.a, self.b)
		else:
			Leg.position(self, self.phiTo, self.aTo, self.bTo)


		
		
	


