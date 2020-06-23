#!/usr/bin/env python
#-*- coding: utf-8 -*-


from legIK import *
import numpy


class WalkCycle :

	distance = 0
	stepHeight = 0
	origin = [0,0,0]
	anim_coord = None


	@staticmethod
	def computeAnimCoord ():

		WalkCycle.anim_coord = [
			[-WalkCycle.distance/2,	0,	0],			#back
			[-WalkCycle.distance/2,	0,	+ WalkCycle.stepHeight],		#go up
			[+WalkCycle.distance/2,	0,	+ WalkCycle.stepHeight], 		#go front
			[+WalkCycle.distance/2,	0,	0] 			#go down
		]
	
	@staticmethod
	def setOrigin(_p) :
		WalkCycle.origin = _p
		WalkCycle.computeAnimCoord()

	@staticmethod
	def setDistance(_d) :
		WalkCycle.distance = _d
		WalkCycle.computeAnimCoord()

	@staticmethod
	def setHeightStep(_h):
		WalkCycle.stepHeight = _h
		WalkCycle.computeAnimCoord()

	@staticmethod
	def getWalkPosition(_leg, _v, _phi, _dir):		#iso to be removed

		'''
		call with  : 
			_leg -> leg object (to find orientation)
			_phi -> give hability to increase or decrease orientation for each Leg
			_v -> évolution of the walCycle from 0 to 100
			_dir -> direction of the walkcycle

			return a value of position in respect with legIK(x, y, z)
		'''

		_v = (float)(_v%100)
		_phi = (float)(_phi)
		_dir = (float)(_dir)

		microstep = (_v%25)/25.0
		inv_microstep = 1-microstep

		local_anim_coord = [0,0,0]

		#find where we are in the animation step
		if _v >= 0 and _v < 25 :
			#go back
			local_anim_coord[0] = WalkCycle.anim_coord[3][0] + ( WalkCycle.anim_coord[0][0] - WalkCycle.anim_coord[3][0] ) * microstep
			local_anim_coord[1] = WalkCycle.anim_coord[3][1] + ( WalkCycle.anim_coord[0][1] - WalkCycle.anim_coord[3][1] ) * microstep
			local_anim_coord[2] = WalkCycle.anim_coord[3][2] + ( WalkCycle.anim_coord[0][2] - WalkCycle.anim_coord[3][2] ) * microstep
		elif _v >= 25 and _v < 50 :
			#go up
			local_anim_coord[0] = WalkCycle.anim_coord[0][0] + ( WalkCycle.anim_coord[1][0] - WalkCycle.anim_coord[0][0] ) * microstep
			local_anim_coord[1] = WalkCycle.anim_coord[0][1] + ( WalkCycle.anim_coord[1][1] - WalkCycle.anim_coord[0][1] ) * microstep
			local_anim_coord[2] = WalkCycle.anim_coord[0][2] + ( WalkCycle.anim_coord[1][2] - WalkCycle.anim_coord[0][2] ) * microstep
		elif _v >= 50  and _v < 75 :
			#go front
			local_anim_coord[0] = WalkCycle.anim_coord[1][0] + ( WalkCycle.anim_coord[2][0] - WalkCycle.anim_coord[1][0] ) * microstep
			local_anim_coord[1] = WalkCycle.anim_coord[1][1] + ( WalkCycle.anim_coord[2][1] - WalkCycle.anim_coord[1][1] ) * microstep
			local_anim_coord[2] = WalkCycle.anim_coord[1][2] + ( WalkCycle.anim_coord[2][2] - WalkCycle.anim_coord[1][2] ) * microstep
		elif _v >= 75 and _v < 100 :
			#go down
			local_anim_coord[0] = WalkCycle.anim_coord[2][0] + ( WalkCycle.anim_coord[3][0] - WalkCycle.anim_coord[2][0] ) * microstep
			local_anim_coord[1] = WalkCycle.anim_coord[2][1] + ( WalkCycle.anim_coord[3][1] - WalkCycle.anim_coord[2][1] ) * microstep
			local_anim_coord[2] = WalkCycle.anim_coord[2][2] + ( WalkCycle.anim_coord[3][2] - WalkCycle.anim_coord[2][2] ) * microstep


		# local_anim_coord[0] = local_anim_coord[0] 
		# local_anim_coord[1] = local_anim_coord[1] 
		# local_anim_coord[2] = local_anim_coord[2] 

		# print(microstep, local_anim_coord)

		'''
		|cos θ   −sin θ   0| |x|   |x cos θ − y sin θ|   |x'|
    	|sin θ    cos θ   0| |y| = |x sin θ + y cos θ| = |y'|
    	|  0       0      1| |z|   |        z        |   |z'|
		'''

		# 1) rotate anim coord around walkcycle origin and value is leg_orient

		local_anim_coord_rotated = [0,0,0]
		angle = math.pi/2 + math.radians( _leg.getOrient()  )  + math.pi/2 * _dir 

		local_anim_coord_rotated[0] = local_anim_coord[0]*math.cos(angle) - local_anim_coord[1] * math.sin(angle)
		local_anim_coord_rotated[1] = local_anim_coord[0]*math.sin(angle) + local_anim_coord[1] * math.cos(angle)
		local_anim_coord_rotated[2] = local_anim_coord[2]

		#transfer local animation to leg origin
		local_anim_coord_rotated[0] = local_anim_coord_rotated[0]+WalkCycle.origin[0]
		local_anim_coord_rotated[1] = local_anim_coord_rotated[1]+WalkCycle.origin[1]
		local_anim_coord_rotated[2] = local_anim_coord_rotated[2]+WalkCycle.origin[2]

		# 2) rotating value around leg origin to appy correction of each leg
		angle = math.radians( _phi ) 
		local_anim_coord_rotated_corrected = [0,0,0]
		local_anim_coord_rotated_corrected[0] = local_anim_coord_rotated[0]*math.cos(angle) - local_anim_coord_rotated[1] * math.sin(angle)
		local_anim_coord_rotated_corrected[1] = local_anim_coord_rotated[0]*math.sin(angle) + local_anim_coord_rotated[1] * math.cos(angle)
		local_anim_coord_rotated_corrected[2] = local_anim_coord_rotated[2]

		return local_anim_coord_rotated_corrected


if __name__ == '__main__':

	import random

	leg_1 = LegIK(24,25,26)
	leg_2 = LegIK(20,21,22)
	leg_3 = LegIK(16,17,18)
	
	leg_4 = LegIK(8, 9, 10)
	leg_5 = LegIK(4, 5, 6)
	leg_6 = LegIK(0, 1, 2)

	leg_1.setOrient(60.0)
	leg_2.setOrient(0.0)
	leg_3.setOrient(-60.0)
	leg_4.setOrient(-120.0)
	leg_5.setOrient(180.0)
	leg_6.setOrient(120.0)

	leg_3.setCorrectionValues([0,5,0],[1,0.95,1])

	LegIK.setAllSpeed(250)

	WalkCycle.setOrigin([40, 0, -60])
	WalkCycle.setHeightStep(30)
	WalkCycle.setDistance(40)


	walk_value = 0

	try :
		while True :


			if LegIK.allReady() :

				dire = 0.5

				leg_1.positionIK( WalkCycle.getWalkPosition( leg_1, walk_value, -50, dire ) )
				leg_2.positionIK( WalkCycle.getWalkPosition( leg_2, walk_value, 0, dire ) )
				leg_3.positionIK( WalkCycle.getWalkPosition( leg_3, walk_value, 30, dire ) )
				leg_4.positionIK( WalkCycle.getWalkPosition( leg_4, walk_value, -40, dire ) )
				leg_5.positionIK( WalkCycle.getWalkPosition( leg_5, walk_value, 0, dire ) )
				leg_6.positionIK( WalkCycle.getWalkPosition( leg_6, walk_value, +40, dire ) )

				LegIK.positionSync()
				walk_value = walk_value + 1


			LegSmooth.updateAll()


		

	except KeyboardInterrupt:

		LegIK.setAllSpeed(75)

		LegIK.allPositionIK([40, 0, -60])
		LegIK.waitUntil()

		#LegIK.allOff()

