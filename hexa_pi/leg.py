#!/usr/bin/env python
#-*- coding: utf-8 -*-


#Dsimonet

#from __future__ import division

from motor import *
from intervallometre import *
import ease

#see here https://stackoverflow.com/questions/739882/iterating-over-object-instances-of-a-given-class-in-python
class IterRegistry(type):
    def __iter__(cls):
        return iter(cls._registry)

######################
"""	LEG """
######################

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


######################
"""	LEG SMOOTH """
######################

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
		LegSmooth._timer = Intervallometre(0.002, LegSmooth.updateSoftAll)
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


######################
"""	LEG IK """
######################

# size in mm and angle in degrees or radian

#			^  0°
#	-x+y	|		+x+y
#			|
#			| XY origin
#  90° -----R--------> 270°
#			|
#	-x-y	|		-y+x
#			|
#		   180°


		#pointXside = math.fabs(x)/x
		#pointYside = math.fabs(y)/y
		#print pointXside, pointYside


class LegIK (LegSmooth):

	robotReverse = 1 #1 for normal side and -1 for reverse

	def __init__(self, _phi, _A, _B, _orient=0):
		LegSmooth.__init__(self, _phi, _A, _B)

		#chain of parent to child is robot -> Coxa -> Femur -> tibia

		#idea is to orient to coxa in direction of the goal
		# and to solve in 2D angle of coxa to femur and femur to tibia to hit the goal

		#pos of leg from robot origin
		# and orientation from origin (front is 0°)
		self.orient = _orient
		self.posX = 0
		self.posY = 0

		self.minRot = -80
		self.maxRot = 80

		self.coxaZ = 11.15

		self.coxaLen = 28.70
		self.femurLen = 41.45
		self.tibiaLen = 47.639

	def SetOrient(self, degres):
		self.orient = degres%360

	def setPosition(self, _x, _y):
		self.posX = _x
		self.posY = _y

	def getSide(self):
		#side : 1 = left, -1 = right
		if self.orient < 180 :
			return 1
		else:
			return -1

	def position(self,_x,_y,_z):



		#computing Orientation of the leg
		#math.atan2(y, x) result -pi to pi 
		goalOrient = math.degrees(math.atan2(math.fabs(_y),math.fabs(_x)))
		goalOrientCorrected = goalOrient - self.orient
		print "goalOrientCorrected",goalOrientCorrected


		#now have to resolve 2 angles of femur & coxa and tibia & femur 
		#but on the same plane.

		#calculate height for coxa from floor (corrected by side of the robot)
		heightCoxa = _z + self.coxaZ*LegIK.robotReverse
		#print "height goal", heightCoxa
		"""
		#calculate air (or floor) distance bettween heightCoxa and goal
		#it's position of robot&coxa axis  (2d) ---> distance (pythagore) minus coxa leng
		lengGoal = math.sqrt( (x-self.posX)*(x-self.posX)+(y-self.posY)*(y-self.posY) ) - self.coxaLen
		print "leng goal", lengGoal

		#calculate 2D distance beetween goal on the floor and axis point of femur& coxa
		distGoal = math.sqrt(  heightCoxa*heightCoxa+lengGoal*lengGoal ) 
		print "dist goal", distGoal

		# calculate angle beetween floor and distance ligne
		angleDistCoxaHeight = math.degrees(math.acos(heightCoxa/distGoal))
		print "angleDistCoxaHeight", angleDistCoxaHeight

		angleGoalFemur = math.degrees(math.acos( (self.tibiaLen*self.tibiaLen - self.femurLen*self.femurLen - distGoal*distGoal)/(-2*self.femurLen*distGoal) ))
		print "angleGoalFemur", angleGoalFemur

		angleFemureCoxa = 90 - (angleDistCoxaHeight + angleGoalFemur)
		print "angleFemureCoxa", angleFemureCoxa

		angleFemurTibia =  math.degrees(math.acos(  (distGoal*distGoal-self.tibiaLen*self.tibiaLen-self.femurLen*self.femurLen)/(-2*self.tibiaLen*self.femurLen) ))
		print "angleFemurTibia", angleFemurTibia

		correctedAngleFemurTibia = 90 - angleFemurTibia
		print "angleFemurTibia", angleFemurTibia
		"""
		LegSmooth.position(self, goalOrientCorrected,0,0)
		#print "------"
		return True


