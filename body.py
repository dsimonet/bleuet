#!/usr/bin/env python
#-*- coding: utf-8 -*-

from patte import *
from intervallometre import *


#on init le system de mise à jour des pattes


class body :

	registry = []

	t =  Intervallometre(0.008, Patte.updateAll)

	def __init__ (self) :

		self.registry.append(Patte(0,0,1,2))
		self.registry.append(Patte(0,4,5,6)) 
		self.registry.append(Patte(0,8,9,10))

		self.t.setDaemon(True)
		self.t.start()

		Patte.speed(16)

		self.Stand()



	def Stand(self) :
		for i in self.registry :
			i.standPosition()

		Patte.waitUntilFinish()

	def Up(self) :
		for i in self.registry :
			i.position(50, 5, 70)

		Patte.waitUntilFinish()


	def Down(self) :
		for i in self.registry :
			i.position(50, 70, 5)

		Patte.waitUntilFinish()