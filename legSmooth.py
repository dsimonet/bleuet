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
		LegSmooth._timer = Intervallometre(0.0001, LegSmooth.updateSoftAll)
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
	def allReady() :
		for leg in LegSmooth :
			if leg._counter == LegSmooth._duration :
				continue
			else:
				return False
		return True


	@staticmethod
	def waitUntilFinish():
		while not LegSmooth.allReady() :
			pass

	@staticmethod
	def updateSoftAll():
		for leg in LegSmooth:
			leg.updateSoft()
	

	def position(self, _phi, _A, _B):

		#stock current position in from value
		self.phiFrom = self.phi
		self.aFrom = self.a
		self.bFrom = self.b

		#stock new position in to value
		self.phiTo = _phi
		self.aTo = _A
		self.bTo = _B

		self._counter = 0

	def orient(self, _phi):
		self.position(_phi, self.aTo, self.bTo)

	def grab(self, _A, _B):
		self.position(self.phiTo, _A, _B)

	def updateSoft(self):

		if(self._duration > 1):
			#compute position from last position trough a ease function
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

		#Moving motor with inherited methode to the computed value
		super(LegSmooth, self).position(self.phi, self.a, self.b)
	


