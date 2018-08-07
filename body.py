#!/usr/bin/env python
#-*- coding: utf-8 -*-

from legSmooth import *
import time


class body :

	def __init__ (self) :
		self.legRegistry = []



	def AddLeg(self, _phi, _A, _B, _orient=0):
		self.legRegistry.append(LegSmooth(_phi, _A, _B))
		time.sleep(0.25) #for avoiding tension drop due current call by all motor moving at the same time by reseting.



# excuted if this doc is not imported
# for testing purpose only
if __name__ == '__main__':

	import time
	import random
	from body import *

	##############################################
	# MAIN
	##############################################


	#create our robot
	bleuet = body()

	# instanciate leg in counter-clockwise  direction

	bleuet.AddLeg(0,1,2) #avant gauche 0
	bleuet.AddLeg(9,10,11) #arrière gauche 1 
	bleuet.AddLeg(6,7,8) #arrière droit 2 
	bleuet.AddLeg(3,4,5) #avant droit 3

	LegSmooth.startThread()

	#walkCycleRegistery = []
	orientation = [1, 1, -1, -1]

	legUp = [-10,20]
	legDown = [20,45]
	frontBack = [20, 0, -20] # 0 = arrière, 1= middle, 2 =avant

	def avancerPatte(_patte, _pose): # -1 = arrière, 0= middle, 1 =avant
		return frontBack[_pose+1]*orientation[_patte]

	LegSmooth.waitUntilFinish()
	LegSmooth.setSpeed(8)

	#Pose initial

	bleuet.legRegistry[0].orient(avancerPatte(0, 0) )
	bleuet.legRegistry[1].orient(avancerPatte(1, 0) )
	bleuet.legRegistry[2].orient(avancerPatte(2, 1))
	bleuet.legRegistry[3].orient(avancerPatte(3, -1))
	LegSmooth.waitUntilFinish()

	for leg in LegSmooth :
		leg.grab(legDown[0], legDown[1])
	LegSmooth.waitUntilFinish()

	# ------

	for r in range(0,10):

		#Avancer une patte
		bleuet.legRegistry[3].grab(legUp[0], legUp[1])
		LegSmooth.waitUntilFinish()
		bleuet.legRegistry[3].orient(avancerPatte(3, 1)) 
		LegSmooth.waitUntilFinish()
		bleuet.legRegistry[3].grab(legDown[0], legDown[1])
		LegSmooth.waitUntilFinish()


		#glisser vers l'avant
		bleuet.legRegistry[0].orient(avancerPatte(0, -1)) #frontBack[0]*orientation[0]
		bleuet.legRegistry[1].orient(avancerPatte(1, -1)) #frontBack[0]*orientation[1]
		bleuet.legRegistry[2].orient(avancerPatte(2, 0)) #frontBack[1]*orientation[1]
		bleuet.legRegistry[3].orient(avancerPatte(3, 0)) #frontBack[1]*orientation[1]
		LegSmooth.waitUntilFinish()

		#rammener une patte
		bleuet.legRegistry[1].grab(legUp[0], legUp[1])
		LegSmooth.waitUntilFinish()
		bleuet.legRegistry[1].orient(avancerPatte(1, 1)) 
		LegSmooth.waitUntilFinish()
		bleuet.legRegistry[1].grab(legDown[0], legDown[1])
		LegSmooth.waitUntilFinish()

		# --

		#Avancer une patte
		bleuet.legRegistry[0].grab(legUp[0], legUp[1])
		LegSmooth.waitUntilFinish()
		bleuet.legRegistry[0].orient(avancerPatte(0, 1)) 
		LegSmooth.waitUntilFinish()
		bleuet.legRegistry[0].grab(legDown[0], legDown[1])
		LegSmooth.waitUntilFinish()


		#glisser vers l'avant
		bleuet.legRegistry[0].orient(avancerPatte(0, 0)) #frontBack[0]*orientation[0]
		bleuet.legRegistry[1].orient(avancerPatte(1, 0)) #frontBack[0]*orientation[1]
		bleuet.legRegistry[2].orient(avancerPatte(2, -1)) #frontBack[1]*orientation[1]
		bleuet.legRegistry[3].orient(avancerPatte(3, -1)) #frontBack[1]*orientation[1]
		LegSmooth.waitUntilFinish()

		#rammener une patte
		bleuet.legRegistry[2].grab(legUp[0], legUp[1])
		LegSmooth.waitUntilFinish()
		bleuet.legRegistry[2].orient(avancerPatte(2, 1)) 
		LegSmooth.waitUntilFinish()
		bleuet.legRegistry[2].grab(legDown[0], legDown[1])
		LegSmooth.waitUntilFinish()


	#Clean end	
	time.sleep(1)
	LegSmooth.closeThread()
	time.sleep(0.2)
	LegSmooth.offAllLegSmooth()
