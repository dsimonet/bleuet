#!/usr/bin/env python
#-*- coding: utf-8 -*-


# Simple demo of of the PCA9685 PWM servo/LED controller library.
# This will move channel 0 from min to max position repeatedly.
# Author: Tony DiCola
# License: Public Domain
from __future__ import division
from threading import Thread
import time
import random
import ease

# Import the PCA9685 module.
import Adafruit_PCA9685

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)


# Helper function to make setting a servo pulse width simpler.
def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)



##############################################
# PATTE
##############################################

class Patte() :

	_registry = []
	_counter = 0
	_duration = 64

	# Configure min and max servo pulse lengths
	servo_min = 120  # Min pulse length out of 4096
	servo_max = 600  # Max pulse length out of 4096

	# Initialise the PCA9685 using the default address (0x40).
	pwm = Adafruit_PCA9685.PCA9685()
	# Alternatively specify a different address and/or bus:
	#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)

	

	def __init__(self, _bus, _phi, _A, _B):

		self.pwm.set_pwm_freq(60)

		#register
		self._registry.append(self)
		self.ready = False
		self.name = "Patte_" + str(len(self._registry)-1)

		#not used yet
		self.bus = _bus

		# les valeurs des moteurs sur la carte de pilotage
		self.motorPhi = _phi
		self.motorA = _A
		self.motorB = _B

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
		for i in Patte._registry:
			i.update()

	@staticmethod
	def speed(v):
		Patte._duration = v

	@staticmethod
	def allReady() :
		for i in Patte._registry :
			if i.ready :
				continue
			else:
				return False
		return True

	@staticmethod
	def waitUntilFinish():
		while not Patte.allReady() :
			None

	@staticmethod
	def allPosition(_phi, _a, _b):
		for p in Patte._registry :
			p.position(_phi, _a, _b)

	#METHODES
	#Convert Value in percent en valeur servo_min et max
	def servoPC(self, v) :	
		return int( Patte.servo_min + v * (Patte.servo_max - Patte.servo_min) / 100 )


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

	def update(self):

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
		

	# POSITION

	def standPosition(self):
		self.position(50,5,70)


