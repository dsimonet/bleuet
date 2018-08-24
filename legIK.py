#!/usr/bin/env python
#-*- coding: utf-8 -*-

from legSmooth import *
import math


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


# excuted if this doc is not imported
# for testing purpose only
if __name__ == '__main__':

	from motor import *
	import time
	from sbus_driver_python import SBUSReceiver


	sbus = SBUSReceiver('/dev/ttyS0')

	def convert(t, a, b, c, d):
		#t moving value
		#a min input
		#b max input
		#c min output
		#d max output
		return c + (t - a) * (d - c) / (b - a)

	# init leg

	leg_1 = LegSmooth(0,1,2)
	leg_1.mot_phi.reverseMotor()


	#init Thread LEG

	LegSmooth.setSpeed(4)
	LegSmooth.startThread()
	LegSmooth.waitUntilFinish()
	
	#make leg move to a position in x y z global (hexapod local)

	time.sleep(1)

	timer1 = time.time()
	timer2 = time.time()+0.1

	while True:


		if sbus.get_rx_channels()[4] >= 512 and sbus.isSync:
			a = convert(sbus.get_rx_channels()[0], 160, 1850, 90,-90)
			b = a
			phi = convert(sbus.get_rx_channels()[1], 160, 1850, -90,90) 
			
			leg_1.position(phi,a,b)


		if time.time() - timer1 > 0.01:
			sbus.get_new_data()
			timer1 = time.time()

		if time.time() - timer2 > 0.2:
			#print a,b, phi
			timer2 = time.time()



	# leg_2.position(-85,0,60)
	# leg_3.position(85,-85,60)
	# leg_4.position(85,0,60)
	
	LegIK.waitUntilFinish()

	#Clean end	
	time.sleep(0.5)
	LegSmooth.closeThread()
	time.sleep(0.2)
	#LegIK.offAllLegSmooth()

