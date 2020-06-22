#!/usr/bin/env python
#-*- coding: utf-8 -*-


from leg import *
import numpy

######################
"""	LEG IK """
######################
'''
 size is in mm angle is radian if possible
 radian range [pi; -pi[
			^  90° / 0
	-x+y	|		+x+y
			|
			| XY origin
 180°-------R--------> 0° /
			|
	-x-y	|		+x-y
			|
		   270°

'''
import math

class LegIK (LegSmooth):

	robotReverse = 1 #1 for normal side and -1 for reverse

	def __init__(self, _phi, _A, _B, _orient=0):
		LegSmooth.__init__(self, _phi, _A, _B)
		'''
		chain of parent to child is robot -> Coxa -> Femur -> tibia
		idea is to orient to coxa in direction of the goal
		and to solve in 2D angle of coxa to femur and femur to tibia to hit the goal

		pos of leg from robot origin
		and orientation from origin (front is 0°)
		'''

		self.orient

		self.minRot = math.radians(-35)
		self.maxRot = math.radians(35)

		self.coxaZ = 18
		self.coxaX = 28.7
		self.coxaLen = 33.88

		self.femurLen = 41.45
		self.tibiaLen = 42+5 #approximated, should be a radius

	def setOrient(self, _orient) :
		self.orient = _orient

	@staticmethod
	def allPositionIk(_x,_y,_z) :
		for leg in LegIK :
			leg.positionIK(_x,_y,_z)

	def getPositionFromDC(self, _phi, _A, _B):
		#ok
		x = self.coxaX + self.femurLen * math.cos(math.radians(_A)) + self.tibiaLen * math.cos(math.radians(_A) + math.radians(_B))
		y = self.coxaZ + self.femurLen * math.sin(math.radians(_A)) + self.tibiaLen * math.sin(math.radians(_A) + math.radians(_B))
		alpha = _A + _B
		return [x, y, alpha]

	def getJoinOrientFromPosition(self, _x, _y, _alpha) :

		_x = _x - self.coxaX
		_y = _y - self.coxaZ

		theta2 = math.pi - math.acos( (self.tibiaLen*self.tibiaLen+self.femurLen*self.femurLen-_x*_x-_y*_y)/(2*self.tibiaLen*self.femurLen)  )
		if _y < 0 :
			theta2 = - theta2
		theta1 = math.radians(_alpha) - theta2

		return [0, math.degrees(theta1), math.degrees(theta2)]

	def positionIK(self,_x,_y,_z):

		#print("called with :", _x, _y, _z)	

		## ORIENTATION CALCULUS

		

		if _x == 0 :
			if _y > 0 :
				localAngle = math.pi/2
			elif _y < 0 :
				localAngle = -math.pi/2
			elif _y == 0 :
				localAngle = 0
		else:
			localAngle = math.atan(_y/_x)

		# if _x == 0 and _y == 0 :
		# 	localAngle = 0;
		# else :

		# 	if not _x == 0 :
		# 		if _x > 0 and _y >= 0 :
		# 			localAngle = math.atan(_y/_x)
		# 		elif _x < 0 and _y >= 0 :
		# 			localAngle = math.pi - math.fabs( math.atan(_y/_x) )
		# 		elif _x < 0 and _y < 0 :
		# 			localAngle = - math.fabs( math.atan(_y/_x) )

		# 	else :
		# 		if _y > 0 :
		# 			localAngle = math.pi/2
		# 		elif _y < 0 :
		# 			localAngle = -math.pi/2
		# 		else :
		# 			localAngle = 0;

		localAngle = localAngle #- math.radians(self.orient)
		#print ("local angle", math.degrees(localAngle ))

		##NOW PASSING TO 2D SOLVING

		## DISTANCE CALCULUS
		local_target_z = _z
		local_target_X  = math.sqrt(_x*_x + _y*_y)	
		#print("local_target_X", local_target_X)
		local_target_dist = math.sqrt(local_target_X*local_target_X+_z*_z)
		#print("local_targetDist", local_target_dist)
		local_target_dist_fromCoxa = math.sqrt( math.pow(local_target_z-self.coxaZ,2)+math.pow(local_target_X-self.coxaX,2) )
		#print("local dist from coxa", local_target_dist_fromCoxa)

		thetaB = math.pi - math.acos( ( math.pow(self.tibiaLen,2)+math.pow(self.femurLen,2)-math.pow(local_target_X-self.coxaX,2)-math.pow(local_target_z-self.coxaZ,2))/(2*self.tibiaLen*self.femurLen)  )
		if _z < 0 :
			thetaB = - thetaB
		#print("thetaB", math.degrees(thetaB))

		Q =  math.acos( (local_target_X-self.coxaX) / local_target_dist_fromCoxa )
		#print ("Local target Z - self.coxaZ :", local_target_X-self.coxaX)
		#print ("Q :", math.degrees(Q))

		thetaA = Q - math.acos((math.pow(self.femurLen,2)-math.pow(self.tibiaLen,2)+math.pow(local_target_dist_fromCoxa,2))/(2*local_target_dist_fromCoxa*self.femurLen))
		if _z < 0 :
			thetaA = - thetaA
		#print("thetaA", math.degrees(thetaA))

		self.position(math.degrees(localAngle ), math.degrees(thetaA) , math.degrees(thetaB) ) 

		#theta1 = math.radians(_alpha) - theta2
		#thetaA = math.pi - 






# excuted if this doc is not imported
# for testing purpose only


if __name__ == '__main__':

	import random

	#  LEG IK TEST

	leg_1 = LegIK(24,25,26)
	leg_2 = LegIK(20,21,22)
	leg_3 = LegIK(16,17,18)
	leg_3.setCorrectionValues([0,5,0],[1,0.95,1])
	leg_4 = LegIK(8, 9, 10)
	leg_5 = LegIK(4, 5, 6)
	leg_6 = LegIK(0, 1, 2)

	LegIK.positionSync()
	LegIK.setAllSpeed(100)
	

	LegIK.allPositionIk(0, 0, -30)
	LegIK.waitUntil()

	LegIK.allPositionIk(20, 0, -70)
	LegIK.waitUntil()

	# try :
	# 	while True :

	# 		LegIK.allPositionIk(20, 0, -70)
	# 		while not LegIK.allReady() :
	# 			LegIK.updateAll()

	# 		LegIK.allPositionIk(20, 0, -50)
	# 		while not LegIK.allReady() :
	# 			LegIK.updateAll()				

	# except KeyboardInterrupt:

	LegIK.setAllSpeed(50)

	for leg in LegIK :
		leg.position(0,0,0)

	while not LegIK.allReady() :
		LegIK.updateAll()

	time.sleep(0.1)

	#LegIK.allOff()

	time.sleep(0.1)