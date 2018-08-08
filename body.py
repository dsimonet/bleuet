#!/usr/bin/env python
#-*- coding: utf-8 -*-

from legSmooth import *
import time


class Body :

	legUp = [-10,20] #value for motor A & B
	legDown = [20,45] #value for motor A & B

	def __init__ (self) :
		self.legRegistry = []
		self.legOrientationRegistery = []

	def AddLeg(self, _phi, _A, _B, _orient=0):
		self.legRegistry.append(LegSmooth(_phi, _A, _B))
		self.legOrientationRegistery.append(_orient)
		time.sleep(0.25) #for avoiding tension drop due current call by all motor moving at the same time by reseting.

	def getSide(self, _leg):
		if self.legOrientationRegistery[_leg] < 180 :
			return 1
		else:
			return -1

	def ReOrient(self, _degre):
		for v in range(0, len(self.legOrientationRegistery)) :
			self.legOrientationRegistery[v] += _degre
			self.legOrientationRegistery[v] %= 360
		
	def LegUp(self, _leg):
		self.legRegistry[_leg].grab(Body.legUp[0], Body.legUp[1])

	def LegDown(self, _leg):
		self.legRegistry[_leg].grab(Body.legDown[0], Body.legDown[1])

	def LegOrient(self, _leg, _degre):
		a = _degre * self.getSide(_leg)
		self.legRegistry[_leg].orient(a)

# excuted if this doc is not imported
# for testing purpose only
if __name__ == '__main__':

	import time
	import random

	##############################################
	# MAIN
	##############################################


	#create our robot
	bleuet = Body()

	# instanciate leg in counter-clockwise  direction
	#with orientation

	bleuet.AddLeg(0,1,2,   60) #avant gauche 0
	bleuet.AddLeg(9,10,11, 120) #arrière gauche 1 
	bleuet.AddLeg(6,7,8,   240) #arrière droit 2 
	bleuet.AddLeg(3,4,5,   300) #avant droit 3

	LegSmooth.startThread()


	LegSmooth.waitUntilFinish()
	LegSmooth.setSpeed(8)

	#Pose initial

	#frontBack = [15, 0, -15] # tree values for phi motor Front, middle, back
	legValueFront = -15 #frontBack[0]
	legValueMiddle = 0 #frontBack[1]
	legValueBack = 15  #frontBack[2]


	#bleuet.ReOrient(+90)


	# bleuet.LegOrient( 0, legValueMiddle)
	# bleuet.LegOrient( 1, legValueMiddle)
	# bleuet.LegOrient( 2, legValueFront)
	# bleuet.LegOrient( 3, legValueBack)
	# LegSmooth.waitUntilFinish()

	for leg in range(0,len(bleuet.legRegistry)) :
		bleuet.LegDown(leg)
	LegSmooth.waitUntilFinish()

	# ------

	for r in range(0,8):


		#find lowest leg 
		firstLeg = bleuet.legOrientationRegistery.index(min(bleuet.legOrientationRegistery))

		#glisser vers l'avant
		bleuet.LegOrient(0, legValueBack)
		bleuet.LegOrient(1, legValueBack)
		bleuet.LegOrient(2, legValueMiddle)
		bleuet.LegOrient(3, legValueMiddle)
		LegSmooth.waitUntilFinish()

		#rammener l'autre patte patte
		bleuet.LegUp(1) 
		LegSmooth.waitUntilFinish()
		bleuet.LegOrient(1, legValueFront)  
		LegSmooth.waitUntilFinish()
		bleuet.LegDown(1)
		LegSmooth.waitUntilFinish()

		#Avancer une patte
		bleuet.LegUp(0) 
		LegSmooth.waitUntilFinish()
		bleuet.LegOrient(0, legValueFront)
		LegSmooth.waitUntilFinish()
		bleuet.LegDown(0)
		LegSmooth.waitUntilFinish()

		#glisser vers l'avant
		bleuet.LegOrient(0, legValueMiddle)
		bleuet.LegOrient(1, legValueMiddle)
		bleuet.LegOrient(2, legValueBack)
		bleuet.LegOrient(3, legValueBack)
		LegSmooth.waitUntilFinish()

		#rammener une patte
		bleuet.LegUp(2) 
		LegSmooth.waitUntilFinish()
		bleuet.LegOrient(2, legValueFront)
		LegSmooth.waitUntilFinish()
		bleuet.LegDown(2) 
		LegSmooth.waitUntilFinish()

		#Avancer une patte
		bleuet.LegUp(3) 
		LegSmooth.waitUntilFinish()
		bleuet.LegOrient(3, legValueFront)  
		LegSmooth.waitUntilFinish()
		bleuet.LegDown(3)
		LegSmooth.waitUntilFinish()



	#Clean end	
	time.sleep(1)
	LegSmooth.closeThread()
	time.sleep(0.2)
	LegSmooth.offAllLegSmooth()
