#!/usr/bin/env python
#-*- coding: utf-8 -*-


from legIK import *
import numpy


class WalkCycle :

	distance = 0
	stepHeight = 0
	origin = [0,0,0]
	
	@staticmethod
	def setOrigin(_p) :
		WalkCycle.origin = _p

	@staticmethod
	def setDistance(_d) :
		WalkCycle.distance = _d

	@staticmethod
	def setHeightStep(_h):
		WalkCycle.stepHeight = _h

	@staticmethod
	def getWalkPosition(_v, _phi, _iso, _dir):		#iso to be removed

		_phi = (float)(_phi)
		_v = (float)(_v)

		_v = _v % 100

		microstep = (_v%25)/25.0
		inv_microstep = 1-microstep
		output = WalkCycle.origin

		anim_coord = [
			[-WalkCycle.distance/2 * microstep,	0,	0],			#back
			[-WalkCycle.distance/2,	0,	+ WalkCycle.stepHeight * microstep],		#go up
			[+WalkCycle.distance/2,	0,	+ WalkCycle.stepHeight * inv_microstep], 		#go front
			[+WalkCycle.distance/2 * inv_microstep,	0,	0] 			#go down
		]

		#rotating the modification around his center
		# and adding them to the position.
		# this is not rotating the origin of the leg
		'''
		|cos θ   −sin θ   0| |x|   |x cos θ − y sin θ|   |x'|
    	|sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
    	|  0       0      1| |z|   |        z        |   |z'|
		'''

		i = 0
		for a in anim_coord :
			out = [0,0,0]
			out[0] = a[0]*math.cos(_phi) - a[1] * math.sin(_phi)
			out[1] = a[0]*math.sin(_phi) + a[1] * math.cos(_phi)
			out[2] = a[2]
			anim_coord[i] = out
			i = i +1 ## ????
			print out

		if _v >= 0 and _v < 25 :
			#go back
			output = [WalkCycle.origin[0]+anim_coord[0][0], WalkCycle.origin[1]+anim_coord[0][1]+_iso, WalkCycle.origin[2]+anim_coord[0][2]]
		elif _v >= 25 and _v < 50 :
			#go up
			output = [WalkCycle.origin[0]+anim_coord[1][0], WalkCycle.origin[1]+anim_coord[1][1]+_iso, WalkCycle.origin[2]+anim_coord[1][2]]
		elif _v >= 50  and _v < 75 :
			#go front
			output = [WalkCycle.origin[0]+anim_coord[2][0], WalkCycle.origin[1]+anim_coord[2][1]+_iso, WalkCycle.origin[2]+anim_coord[2][2]]
		elif _v >= 75 and _v < 100 :
			#go down
			output = [WalkCycle.origin[0]+anim_coord[3][0], WalkCycle.origin[1]+anim_coord[3][1]+_iso, WalkCycle.origin[2]+anim_coord[3][2]]

		#print(_v, microstep, output)

		return output


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

	# LegIK.allPositionIK(0, 0, -30)
	# LegIK.waitUntil()

	# LegIK.allPositionIK(20, 0, -70)
	# LegIK.waitUntil()


	WalkCycle.setOrigin([40, 0, -60])
	WalkCycle.setDistance(40)



	walk_value = 0
	# t0 = 0
	# t1 = 0
	try :
		while True :


			if LegIK.allReady() :
				leg_1.positionIK( WalkCycle.getWalkPosition( walk_value, math.radians(90-20), -20 ) )
				leg_2.positionIK( WalkCycle.getWalkPosition( walk_value+50, math.radians(90-20), 0 ) )
				leg_3.positionIK( WalkCycle.getWalkPosition( walk_value, math.radians(90-20), +20 ) )

				leg_4.positionIK( WalkCycle.getWalkPosition( walk_value+50, math.radians(-90-20), -20 ) )
				leg_5.positionIK( WalkCycle.getWalkPosition( walk_value, math.radians(-90-20), 0 ) )
				leg_6.positionIK( WalkCycle.getWalkPosition( walk_value+50, math.radians(-90-20), +20 ) )

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

		LegIK.allPositionIK([40, 0, -60])
		LegIK.waitUntil()

		#LegIK.allOff()

