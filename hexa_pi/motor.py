#!/usr/bin/env python
#-*- coding: utf-8 -*-


#dsimonet motor moving class from adafruit example and library

# Import the PCA9685 module.
import Adafruit_PCA9685



##############################################
# Motor
##############################################

class Motor :

	#library who drive motor in low level I2C
	pwm = Adafruit_PCA9685.PCA9685()


	# in calculation of move, some ratio value are calculate a every move but not change
	# so we added a précalculate value of them
	preComputedScaleValue = None

	def __init__ (self, _pin, freq=60):
		Motor.pwm.set_pwm_freq(freq)
		self.pin = _pin
		self.value = None	#last position received 
		self.position = None	#last position sent

		#minimal/maximal input default value 
		self.ctrl_min_value = -90
		self.ctrl_max_value = 90

		#minimal/maximal output PWM default value
		#starting a 100 because between 0 and value near 30 mlservo is off and position is evaluate between this range.
		#so you have a dead zone beatween 0 to 30 and 100 to 600
		self.servo_min = 130 
		self.servo_max = 630

		# précomputing of one value used in move
		#self.computeScaleValue()	

	#tweaking methodes values
	def setMinMaxInput(self, min, max):
		self.ctrl_min_value = min
		self.ctrl_max_value = max

	def setMinMaxOutput(self, min, max):
		self.servo_min = min
		self.servo_max = max

	def move(self, v):
		self.value = v
		self.position =  self.servo_min + (v - self.ctrl_min_value) * (self.servo_max - self.servo_min) / (self.ctrl_max_value - self.ctrl_min_value) 
		Motor.pwm.set_pwm(self.pin, 1, int(self.position) )

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
		Motor.pwm.set_pwm(self.pin, 1, int(v) )
	
	#value between dead zone make motor off. 0 & 0 make pwm ratio to zero so motor stop
	def off(self):
		Motor.pwm.set_pwm(self.pin, 0, 0)
	#get back the inital value
	def on(self) :
		self.move(self.value)

	#reset motor position by sending center value of min/max input to move methode
	def reset(self) :
		self.move(self.ctrl_min_value + (self.ctrl_max_value-self.ctrl_min_value)/2 )

	# change side mouvement of motor
	def reverseMotor(self):
		temp = self.ctrl_min_value
		self.ctrl_min_value = self.ctrl_max_value
		self.ctrl_max_value = temp
