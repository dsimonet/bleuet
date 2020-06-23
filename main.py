#!/usr/bin/env python
#-*- coding: utf-8 -*-

# from __future__ import division

import time
import random
from hexa_pi import *
from sbusPythonDriver import *
from threading import *

# init leg
# number is the port on PCA card used by this leg
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

#sbus to catch info from frSky receiver
sbus = SBUSReceiver('/dev/ttyS0')

############
# Thread declaration
############
'''
create threading function for updatting LEG and SBUS values.
Because of the python GLI interpreter and because Raspberry pi Zero have only one core
multitrheading make the update function slower than put in the main loop.
''' 

# sbusUpdate_continue = True
# class sbusUpdateThread(Thread) :
# 	def __init__(self):
# 		Thread.__init__(self)

# 	def run(self):
# 		while sbusUpdate_continue:
# 			sbus.update()

# #Leg smooth is threaded for perfomance issues
#  # this alow to stop this thread
# LegSmooth_continue = True
# class legUpdateThread(Thread) :
# 	def __init__(self):
# 		Thread.__init__(self)

# 	def run(self):
# 		while LegSmooth_continue:
# 			if not LegSmooth.allReady() :
# 				LegSmooth.updateAll()



# sbusUpdateThread_instance = sbusUpdateThread()
# LegSmoothThread_instance = legUpdateThread()

# sbusUpdateThread_instance.start()
# LegSmoothThread_instance.start()


##############################################
# MAIN
##############################################
'''
create threading function for updatting LEG and SBUS values.
Because of the python GLI interpreter and because Raspberry pi Zero have only one core
multitrheading make the update function slower than put in the main loop.
''' 

if __name__ == '__main__':

	timerFSM = time.clock()
	timerSbus = time.clock()

	walk_value = 0
	WalkCycle.setOrigin([40, 0, -60])
	WalkCycle.setDistance(40)
	WalkCycle.setHeightStep(20)

	try :
		while True :

			LegIK.updateAll()
			
			if(time.clock() - timerSbus > 0.1) :
				timerSbus = time.clock()
				sbus.update()



			if time.clock() - timerFSM > 0.001 :
				timerFSM = time.clock()

				#in any other case (receiver lost)
				if sbus.get_failsafe_status() == 1 :

					print("No connexion with remote controler")

					LegSmooth.setAllSpeed(50)

					for leg in LegSmooth:
						leg.position(0,0,0)

				#if Switch F is up and not receiver is not lost
				elif sbus.get_rx_channels()[15] > 512  :

					#speed from pot S1
					LegSmooth.setAllSpeed( remap(sbus.get_rx_channels()[14], 172, 1811, 5, 600) )

					h = remap(sbus.get_rx_channels()[0], 172, 1811, 35, 60)
					WalkCycle.setOrigin([40, 0, -h])

					h2 = remap(sbus.get_rx_channels()[5], 172, 1811, 0, 60)
					WalkCycle.setHeightStep( h2 )

					dir = remap(sbus.get_rx_channels()[3], 172, 1811, -1.0, +1.0)
					
					leg_1.positionIK( WalkCycle.getWalkPosition( leg_1, walk_value+100*0/6, -50, dir ) )
					leg_2.positionIK( WalkCycle.getWalkPosition( leg_2, walk_value+100*1/6, 0, dir ) )
					leg_3.positionIK( WalkCycle.getWalkPosition( leg_3, walk_value+100*2/6, 30, dir ) )
					leg_4.positionIK( WalkCycle.getWalkPosition( leg_4, walk_value+100*5/6, -40, dir ) )
					leg_5.positionIK( WalkCycle.getWalkPosition( leg_5, walk_value+100*4/6, 0, dir ) )
					leg_6.positionIK( WalkCycle.getWalkPosition( leg_6, walk_value+100*3/6, +40, dir ) )

					LegIK.positionSync()
					if LegSmooth.allReady() :
						pass
					walk_value += remap(sbus.get_rx_channels()[2], 172, 1811, -5, 5)
					walk_value %= 100


				#if Switch F is down and not receiver is not lost
				elif sbus.get_rx_channels()[15] < 512 :

					#speed from pot S1
					LegSmooth.setAllSpeed( remap(sbus.get_rx_channels()[14], 172, 1811, 5, 500) )

					h = remap(sbus.get_rx_channels()[0], 172, 1811, 0, 80)
					for leg in LegSmooth:
						leg.position(0,-h,-90+h)




	except KeyboardInterrupt:
		# sbusUpdateThread_instance.cancel()
		# LegSmooth_continue = False
		# sbusUpdate_continue = False

		# LegSmoothThread_instance.join()
		# sbusUpdateThread_instance.join()
		pass

