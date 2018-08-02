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

class motor :

	__metaclass__ = IterRegistry
	_registry = []

	#library who drive motor in low level I2C
	pwm = Adafruit_PCA9685.PCA9685()


	# in calculation of move, some ratio value are calculate a every move but not change
	# so we added a précalculate value of them
	preComputedScaleValue = None

	def __init__ (self, _pin, freq=60):
		self._registry.append(self)
		self.pwm.set_pwm_freq(freq)
		self.pin = _pin
		self.value = None	#last position received 
		self.position = None	#last position sent

		#minimal/maximal input default value 
		self.ctrl_min_value = -50
		self.ctrl_max_value = 50

		#minimal/maximal output PWM default value
		#starting a 100 because between 0 and value near 30 mlservo is off and position is evaluate between this range.
		#so you have a dead zone beatween 0 to 30 and 100 to 600
		self.servo_min = 120  
		self.servo_max = 620

		# précomputing of one value used in move
		self.computeScaleValue()	

	#tweaking methodes values
	def setMinMaxInput(self, min, max):
		motor.ctrl_min_value = min
		motor.ctrl_max_value = max
		self.computeScaleValue()

	def setMinMaxOutput(self, min, max):
		motor.servo_min = min
		motor.servo_max = max
		self.computeScaleValue()

	def move(self, v):
		self.value = v
		self.position =  self.servo_min + (v - self.ctrl_min_value) * self.preComputedScaleValue # <-- see the précaculate value
		self.pwm.set_pwm(self.pin, 1, int(self.position) )

	def safeMove(self, v):
		if v < self.ctrl_min_value:
			v = self.ctrl_min_value
		if v > self.ctrl_max_value:
			v = self.ctrl_max_value
		self.move(v)

	# this fonction alow to move the motor witout percent value but with raw data
	# use with caution can block or damage motor if set PWM value under move capability
	#but reconized by servo as valid move (not in off range)
	def moveRaw(self, v):
		self.pwm.set_pwm(self.pin, 1, int(v) )
	
	#value between dead zone make motor off. 0 & 0 make pwm ratio to zero so motor stop
	def off(self):
		self.pwm.set_pwm(self.pin, 0, 0)
	#get back the inital value
	def on(self) :
		self.move(self.value)

	#reset motor position by sending center value of min/max input to move mthode
	def reset(self) :
		self.move(self.ctrl_min_value + (self.ctrl_max_value-self.ctrl_min_value)/2 )

	def computeScaleValue(self):
		self.preComputedScaleValue =  (self.servo_max - self.servo_min) / (self.ctrl_max_value - self.ctrl_min_value)

	# change side mouvement of motor
	def reverseMotor(self):
		temp = self.ctrl_min_value
		self.ctrl_min_value = self.ctrl_max_value
		self.ctrl_max_value = temp

		self.computeScaleValue()

#excuted if this doc is not imported
if __name__ == '__main__':

	import time

	phi = motor(0)
	motA = motor(1)
	motB = motor(2)
	motB.reverseMotor()

	for i in range(-50,50):
		phi.move(i)
		motA.move(i)
		motB.move(i)
		time.sleep(0.1)

	phi.move(10)
	motA.move(10)
	motB.move(10)

	for i in motor :
		i.reset()