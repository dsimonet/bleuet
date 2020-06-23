#!/usr/bin/env python
#-*- coding: utf-8 -*-


from legIK import *
import numpy


class WalkCycle :

	origin = [0,0,0]
	
	@staticmethod
	def setOrigin(_p) :
		WalkCycle.origin = _p


	@staticmethod
	def getWalkPosition(_v, _phi):

		_v = _v % 100

		microstep = (_v%25)/25.0
		inv_microstep = 1-microstep
		output = WalkCycle.origin

		if _v > 0 and _v < 25 :
			#go back
			output = [WalkCycle.origin[0]-50, WalkCycle.origin[1], WalkCycle.origin[2]]
		elif _v >= 25 and _v < 50 :
			#go up
			output = [WalkCycle.origin[0]-50, WalkCycle.origin[1], WalkCycle.origin[2]+20]
		elif _v >= 50  and _v < 75 :
			#go front
			output = [WalkCycle.origin[0]-50, WalkCycle.origin[1], WalkCycle.origin[2]+20]
		elif _v >= 75 and _v < 100 :
			#go down
			output = [WalkCycle.origin[0], WalkCycle.origin[1], WalkCycle.origin[2]+20]
		else : 
			output = WalkCycle.origin

		#print(_v, microstep, output)
		'''
		|cos θ   −sin θ   0| |x|   |x cos θ − y sin θ|   |x'|
    	|sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
    	|  0       0      1| |z|   |        z        |   |z'|
		'''
		output_r = [0,0,0]
		output_r[0] = output[0]*math.cos(_phi) - output[1] * math.sin(_phi)
		output_r[1] = output[0]*math.sin(_phi) + output[1] * math.cos(_phi)
		output_r[2] = output[2]
		return output_r
		#return WalkCycle.origin


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
	LegIK.setAllSpeed(600)

	# LegIK.allPositionIK(0, 0, -30)
	# LegIK.waitUntil()

	# LegIK.allPositionIK(20, 0, -70)
	# LegIK.waitUntil()


	WalkCycle.setOrigin([70, 0, -60])

	walk_value = 0
	t0 = 0
	t1 = 0
	try :
		while True :

			if LegIK.allReady() :
				
				leg_1.positionIK( WalkCycle.getWalkPosition( walk_value, math.radians(-15) ) )

				LegIK.positionSync()
				walk_value = walk_value + 25



			LegSmooth.updateAll()

			#print(leg, time.clock() - t0)

			# p = WalkCycle.getWalkPosition( walk_value )
			# LegIK.allPositionIK(p[0], p[1], p[2])
			# LegSmooth.positionSync()
			
			# t0 = time.clock()
			# while not LegIK.allReady()  :
			# 	LegIK.updateAll()
			# print(time.clock() - t0 )

		

	except KeyboardInterrupt:

		LegIK.setAllSpeed(75)

		LegIK.allPosition(0,0,0)
		LegIK.waitUntil()

		LegIK.allOff()

