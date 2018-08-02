#!/usr/bin/env python
#-*- coding: utf-8 -*-


#dsimonet motor moving class from adafruit example and library

# Import the PCA9685 module.
import Adafruit_PCA9685


class motor :

	#library who drive motor in low level I2C
	pwm = Adafruit_PCA9685.PCA9685()

	#minimal/maximal input default value 
	ctrl_min_value = 0
	ctrl_max_value = 100

	#minimal/maximal output PWM default value
	#starting a 100 because between 0 and value near 30 mlservo is off and position is evaluate between this range.
	#so you have a dead zone beatween 0 to 30 and 100 to 600
	servo_min = 120  
	servo_max = 620 

	# in calculation of move, some ratio value are calculate a every move but not chang
	# so we added a précalculate value of them
	preComputedScaleValue = None

	def __init__ (self, _pin, freq=60):
		self.pwm.set_pwm_freq(freq)
		self.pin = _pin
		self.value = None	#last position received 
		self.position = None	#last position sent
		self.preComputedScaleValue =  (self.servo_max - self.servo_min) / (self.ctrl_max_value - self.ctrl_min_value)	# précomputing of one value used in move

	#tweaking meathodes but affect every instance of motor
	@staticmethod
	def setMinMaxInput(min, max):
		motor.ctrl_min_value = min
		motor.ctrl_max_value = max

	@staticmethod
	def setMinMaxOutput(min, max):
		motor.servo_min = min
		motor.servo_max = max

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



"""

#excuted if this doc is not imported
if __name__ == '__main__':

	import time

	phi1 = motor(2)
	motor.setMinMaxInput(-50,50)

	phi1.move(0)
	time.sleep(0.5)
	phi1.safeMove(250)
	time.sleep(10)
	phi1.move(25)
	time.sleep(0.5)

	phi1.off()
	time.sleep(1)
	phi1.on()
	time.sleep(1)
	
	for i in range(-50,50):
		phi1.move(i)
		time.sleep(0.1)
"""