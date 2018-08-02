#!/usr/bin/env python
#-*- coding: utf-8 -*-

from leg import *
#from intervallometre import *


#on init le system de mise à jour des Legs


class body :

	#t =  Intervallometre(0.008, Patte.updateAll)

	def __init__ (self) :

		self.registry = []
		#self.t.setDaemon(True)
		#self.t.start()

		#Leg.speed(16)

		#self.Stand()


	def AddLeg(self, _bus, _phi, _A, _B):
		self.registry.append(Leg(_bus, _phi, _A, _B))


	def Stand(self) :
		for i in self.registry :
			i.standPosition()

		#Leg.waitUntilFinish()

	def Up(self) :
		for i in self.registry :
			i.position(50, 5, 70)

		#Leg.waitUntilFinish()


	def Down(self) :
		for i in self.registry :
			i.position(50, 70, 5)

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


	bleuet = body()
	bleuet.AddLeg(0,0,1,2)
	bleuet.AddLeg(0,4,5,6)
	bleuet.AddLeg(0,8,9,10)


	bleuet.Down()
	time.sleep(1)
	bleuet.Up()
	time.sleep(1)
	bleuet.Down()
	time.sleep(1)
	bleuet.Stand()