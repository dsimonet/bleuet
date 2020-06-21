#!/usr/bin/env python
#-*- coding: utf-8 -*-


#dsimonet motor moving class from adafruit example and library

# Import the PCA9685 module.
import Adafruit_PCA9685


#see here https://stackoverflow.com/questions/739882/iterating-over-object-instances-of-a-given-class-in-python
class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

##############################################
# Motor
##############################################

class Motor :

	#library who drive motor in low level I2C
	pwm = [ Adafruit_PCA9685.PCA9685() ]

	# for iterate over instances
	__metaclass__ = IterRegistry
	_registry = []

	def __init__ (self, _pin, freq=60):
		"""
		pin goes from 0 to 15 for bus 1 and for each group of 16 next values
		bus is automaticaly incremented by one
		start address is 0x40 (10b64) next is 0x41 (10b65) etc.
		"""
		#iteration append
		MotorSmooth._registry.append(self)

		#motor bus and pin
		self.bus = int(_pin//16) # int 64 = 0x40 in hex
		for i in range(self.bus):
			if not len(Motor.pwm) < self.bus:
				Motor.pwm.append( Adafruit_PCA9685.PCA9685(64+self.bus) )
		
		Motor.pwm[self.bus].set_pwm_freq(freq)
		self.pin = _pin - 16*self.bus

		#motor position
		self.value = 0	#last position sent
		self.backupValue = 0	#last position received 

		#minimal/maximal input default value 
		self.ctrl_min_value = -90
		self.ctrl_max_value = 90

		#minimal/maximal output PWM default value
		#starting a 100 because between 0 and value near 30 mlservo is off and position is evaluate between this range.
		#so you have a dead zone bettween 0 to 30 and 100 to 600
		self.servo_min = 130 
		self.servo_max = 630

		#motor side
		self.side = True

		self.reset()

	def __del__(self):
		off(self)

	#tweaking methodes values
	def setMinMaxInput(self, min, max):
		self.ctrl_min_value = min
		self.ctrl_max_value = max

	def setMinMaxOutput(self, min, max):
		self.servo_min = min
		self.servo_max = max

	def move(self, _v):
		self.value = _v
		computed = self.servo_min + (self.value - self.ctrl_min_value) * (self.servo_max - self.servo_min) / (self.ctrl_max_value - self.ctrl_min_value)
		Motor.pwm[self.bus].set_pwm(self.pin, 1, int(computed) )

	def safeMove(self, v):
		if v < self.ctrl_min_value:
			v = self.ctrl_min_value
		if v > self.ctrl_max_value:
			v = self.ctrl_max_value
		self.move(v)

	# this fonction alow to move the motor witout percent value but with raw data
	# use with caution can block or damage motor if set PWM value under move capability
	# but reconized by servo as valid move (not in off range)
	def moveRaw(self, v):
		Motor.pwm[self.bus].set_pwm(self.pin, 1, int(v) )
	
	#value between dead zone make motor off. 0 & 0 make pwm ratio to zero so motor stop
	def off(self):
		self.backupValue = self.value
		Motor.pwm[self.bus].set_pwm(self.pin, 0, 0)
	#get back the inital value
	def on(self) :
		self.value = self.backupValue
		Motor.pwm[self.bus].set_pwm(self.pin, 0, int(self.value))

	#reset motor position by sending center value of min/max input to move methode
	def reset(self) :
		self.move(self.ctrl_min_value + (self.ctrl_max_value-self.ctrl_min_value)/2 )

	# change side mouvement of motor
	def reverseMotor(self):
		temp = self.ctrl_min_value
		self.ctrl_min_value = self.ctrl_max_value
		self.ctrl_max_value = temp

	def setSide(self, _side):
		if self.side :
			self.reverseMotor()
			self.side = _side
		else:
			self.reverseMotor()
			self.side = _side
			
		# if self.ctrl_min_value < self.ctrl_max_value :
		# 	if not side :
		# 		
		# else :
		# 	if side :
		# 		self.reverseMotor()

######################
"""	MOTOR SMOOTH """
######################


import time
import ease

class MotorSmooth(Motor):

	@staticmethod
	def updateAll():
		for m in Motor :
			m.update()

	@staticmethod
	def setAllSpeed(value):
		if not value == 0:
			for motor in MotorSmooth:
				motor.speed = value

	# -----------

	def __init__(self, _pin, freq=60):
		Motor.__init__(self, _pin, freq)

		#values
		self.speed = 150.0 #mm/s or degres/s --> 9G servo is 0.12second/ 60degree = 500 °/S
		self.duration = 0.0
		self.timeBegin = 0.0

		self.fromValue = self.value
		self.goalValue = self.value

		self.move(self.value)

	def setSpeed(self, value):
		if not value == 0:
			self.speed = float(value)

	def position(self, _v):
		self.timeBegin = time.time()

		self.fromValue = self.value
		self.goalValue = _v

		self.duration = abs(self.fromValue - self.goalValue)/self.speed


	def update(self):
		#compute position from last position trough a ease function
		#
		# t is the current time (or position) of the tween.   CURSOR
		# b is the beginning value of the property.    FROM
		# c is the change between the beginning and destination value of the property. TO
		# d is the total time of the tween. MAX CURSOR
		if time.time() < (self.timeBegin + self.duration) :
			self.value = ease.easeInOutQuad( time.time()-self.timeBegin, self.fromValue, self.goalValue-self.fromValue, self.duration )
			Motor.move(self, self.value)

	def isReady(self):
		return time.time() >= (self.timeBegin + self.duration)

	@staticmethod
	def sync(*args):
		# for any number of args
		# seach  for the longest travel to do.
		# and apply it to all the motorSmooth passed in args
		maxValue = 0
		for arg in args :
			if  arg.duration > maxValue :	
				maxValue = arg.duration
		
		for arg in args:
			arg.duration = maxValue




# excuted if this doc is not imported
# for testing purpose only
if __name__ == '__main__':

	import random

	m1 = MotorSmooth(0)
	m2 = MotorSmooth(1)
	m3 = MotorSmooth(2)

	timer0 = 0
	timer1 = 0

	try :
		while True :
			
			#every 2 second we change position
			if time.time()-timer0 >= 2:
				m1.position(random.randint(-60,60))
				m2.position(random.randint(-60,60))
				m3.position(random.randint(-60,60))
				
				print(m1.goalValue, m2.goalValue, m3.goalValue)
				
				MotorSmooth.sync(m1, m2, m3)

				timer0 = time.time()

			#every millis we update motor position
			if time.time()-timer1 >= 0.001:
				MotorSmooth.updateAll()
				timer1 = time.time()

	except KeyboardInterrupt:
		pass