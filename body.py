#!/usr/bin/env python
#-*- coding: utf-8 -*-

from legSmooth import *


class body :

	def __init__ (self) :
		self.legRegistry = []


	def AddLeg(self, _phi, _A, _B):
		self.legRegistry.append(LegSmooth(_phi, _A, _B))


	def Stand(self) :
		for i in self.legRegistry :
			pass

		#Leg.waitUntilFinish()

	def Up(self) :
		for i in self.legRegistry :
			i.position(0, -30, 20)

		#Leg.waitUntilFinish()


	def Down(self) :
		for i in self.legRegistry :
			i.position(0, 10, 20)

		#Leg.waitUntilFinish()


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

	# instanciate leg in clockwise  direction

	bleuet.AddLeg(3,4,5)
	bleuet.AddLeg(6,7,8)
	bleuet.AddLeg(9,10,11)
	bleuet.AddLeg(0,1,2)




	walkCycleRegistery = []

	orientation = [60, 120, -120, -60]
	
	walkCycleRegistery.append( [-15, 0, 50] )
	walkCycleRegistery.append( [15, 0, 50] )
	walkCycleRegistery.append( [15, 40, 10] )
	walkCycleRegistery.append( [-15, 40 ,10] )

	for rep in range(0,10): # repeating 3 times
		for cycle in range(0,len(walkCycleRegistery)) : # for each walk cycle step 
			for leg in range(0, len(bleuet.legRegistry)) : # for each
				if orientation[leg] > 0: #if leg is on one side or other
					if leg%2 == 0 :	# if leg is odd or even
						bleuet.legRegistry[leg].position( walkCycleRegistery[cycle][0], walkCycleRegistery[cycle][1], walkCycleRegistery[cycle][2])
					else :
						a = (cycle+2)%(len(walkCycleRegistery))
						bleuet.legRegistry[leg].position( walkCycleRegistery[a][0], walkCycleRegistery[a][1], walkCycleRegistery[a][2])
				else :
					if leg%2 == 0 :
						bleuet.legRegistry[leg].position( -walkCycleRegistery[cycle][0], walkCycleRegistery[cycle][1], walkCycleRegistery[cycle][2])
					else:
						a = (cycle+2)%(len(walkCycleRegistery))
						bleuet.legRegistry[leg].position( -walkCycleRegistery[a][0], walkCycleRegistery[a][1], walkCycleRegistery[a][2])
			time.sleep(0.25)



	for leg in Leg :
		leg.orient(0)

	time.sleep(1)


	for leg in Leg :
		leg.off()