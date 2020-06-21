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
leg_1 = LegSmooth(0,1,2)
leg_2 = LegSmooth(4,5,6)
leg_3 = LegSmooth(8,9,10)
leg_4 = LegSmooth(16, 17, 18)
leg_5 = LegSmooth(20, 21, 22)
leg_6 = LegSmooth(24, 25, 26)

leg_1.mot_phi.reverseMotor()
leg_2.mot_phi.reverseMotor()
leg_3.mot_phi.reverseMotor()
leg_4.mot_phi.reverseMotor()
leg_5.mot_phi.reverseMotor()
leg_6.mot_phi.reverseMotor()

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

sbusUpdate_continue = True
class sbusUpdateThread(Thread) :
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		while sbusUpdate_continue:
			sbus.update()
			#time sleep block this thread and permit to select prorities
			time.sleep(0.5)

#Leg smooth is threaded for perfomance issues
 # this alow to stop this thread
LegSmooth_continue = True
class legUpdateThread(Thread) :
	def __init__(self):
		Thread.__init__(self)

	def run(self):
		while LegSmooth_continue:
			if not LegSmooth.allReady() :
				LegSmooth.updateAll()
			#time sleep block this thread and permit to select prorities
			#time.sleep(0.0001)



# sbusUpdateThread_instance = sbusUpdateThread()
LegSmoothThread_instance = legUpdateThread()

# sbusUpdateThread_instance.start()
LegSmoothThread_instance.start()

############
# WalkCycle
############
'''

''' 

def walkCycle(h, v):

	majorStep = 100.0/4.0
	subStep =  majorStep/3.0
	microStep = remap((v%majorStep)%subStep, 0, subStep, 0, 1)

	print( "majorStep : % 5.2f, subStep : % 5.2f" %(v, microStep) )  
	upAPosition = 10
	upBPosition = -80
	downAPosition = -h
	downBPosition = -90+h
	phiFront = 20
	phiBack = -20

	if v < majorStep :
		leg_1.position(phiFront,downAPosition,downBPosition)
		leg_3.position(phiFront,downAPosition,downBPosition)
		leg_5.position(-phiFront,downAPosition,downBPosition)

		leg_2.position(phiBack,upAPosition,upBPosition)
		leg_4.position(-phiBack,upAPosition,upBPosition)
		leg_6.position(-phiBack,upAPosition,upBPosition)

	elif v > majorStep and v < majorStep*2:
		leg_1.position(phiBack,downAPosition,downBPosition)
		leg_3.position(phiBack,downAPosition,downBPosition)
		leg_5.position(-phiBack,downAPosition,downBPosition)

		leg_2.position(phiFront,upAPosition,upBPosition)
		leg_4.position(-phiFront,upAPosition,upBPosition)
		leg_6.position(-phiFront,upAPosition,upBPosition)

	elif v > majorStep*2 and v < majorStep * 3:
		leg_1.position(phiBack,upAPosition,upBPosition)
		leg_3.position(phiBack,upAPosition,upBPosition)
		leg_5.position(-phiBack,upAPosition,upBPosition)

		leg_2.position(phiFront,downAPosition,downBPosition)
		leg_4.position(-phiFront,downAPosition,downBPosition)
		leg_6.position(-phiFront,downAPosition,downBPosition)

	elif v > majorStep*3 :
		leg_1.position(phiFront,upAPosition,upBPosition)
		leg_3.position(phiFront,upAPosition,upBPosition)
		leg_5.position(-phiFront,upAPosition,upBPosition)

		leg_2.position(phiBack,downAPosition,downBPosition)
		leg_4.position(-phiBack,downAPosition,downBPosition)
		leg_6.position(-phiBack,downAPosition,downBPosition)


'''
	#move odd leg
	# [0 to 25[
	if v < majorStep :
		if v < subStep :	#up
			leg_1.position(phiBack-10,upAPosition*microStep,upBPosition*microStep)
			# leg_3.position(phiBack,upAPosition*microStep,upBPosition*microStep)
			# leg_5.position(-phiBack,upAPosition*microStep,upBPosition*microStep)
		elif v < subStep*2 :	#front
			leg_1.position(phiFront-10,upAPosition,upBPosition)
			# leg_3.position(phiFront,upAPosition,upBPosition)
			# leg_5.position(-phiFront,upAPosition,upBPosition)
		elif v < subStep*3 :	#down
			leg_1.position(phiFront-10,downAPosition,downBPosition)
			# leg_3.position(phiFront,downAPosition,downBPosition)
			# leg_5.position(-phiFront,downAPosition,downBPosition)
			
		#redefining other legs in any case	
		# leg_2.position(phiFront,downAPosition,downBPosition)
		# leg_4.position(-phiFront,downAPosition,downBPosition)
		leg_6.position(-phiFront,downAPosition,downBPosition)

		

	#move body front
	# [25 to 50[
	elif v > majorStep and v < majorStep*2:
		leg_1.position(phiBack,downAPosition,downBPosition)
		# leg_2.position(phiBack,downAPosition,downBPosition)
		# leg_3.position(phiBack,downAPosition,downBPosition)
		# leg_4.position(-phiBack,downAPosition,downBPosition)
		# leg_5.position(-phiBack,downAPosition,downBPosition)
		leg_6.position(-phiBack,downAPosition,downBPosition)

	#move even leg
	# [50 to 75[
	elif v > majorStep*2 and v < majorStep * 3:
		if v < majorStep*2 + subStep :	#up
			pass
			# leg_2.position(-phiFront,upAPosition,upBPosition)
			# leg_4.position(phiFront,upAPosition,upBPosition)
			leg_6.position(phiFront,upAPosition,upBPosition)
		elif v < majorStep*2 + subStep*2 :	#front
			pass
			# leg_2.position(-phiBack,upAPosition,upBPosition)
			# leg_4.position(phiBack,upAPosition,upBPosition)
			leg_6.position(phiBack,upAPosition,upBPosition)
		elif v < majorStep*2 + subStep*3 :	#down
			pass
			# leg_2.position(-phiBack,downAPosition,downBPosition)
			# leg_4.position(phiBack,downAPosition,downBPosition)
			leg_6.position(phiBack,downAPosition,downBPosition)
			
		#redefining other legs in any case	
		leg_1.position(phiBack,downAPosition,downBPosition)
		# leg_3.position(phiBack,downAPosition,downBPosition)
		# leg_5.position(-phiBack,downAPosition,downBPosition)

	#move body front
	# [75 to 100[
	elif v > majorStep*3 :
		leg_1.position(phiBack,downAPosition,downBPosition)
		# leg_2.position(phiBack,downAPosition,downBPosition)
		# leg_3.position(phiBack,downAPosition,downBPosition)
		# leg_4.position(-phiBack,downAPosition,downBPosition)
		# leg_5.position(-phiBack,downAPosition,downBPosition)
		leg_6.position(-phiBack,downAPosition,downBPosition)

'''

##############################################
# MAIN
##############################################
'''
create threading function for updatting LEG and SBUS values.
Because of the python GLI interpreter and because Raspberry pi Zero have only one core
multitrheading make the update function slower than put in the main loop.
''' 


if __name__ == '__main__':

	timer0 = time.time()
	timer1 = time.time()

	LegSmooth.setAllSpeed(250)
	walkStep = 0

	try :
		while True :

			#for testing wol cycle

			#if time.time() - timer0 > 0.1 :
			if LegSmooth.allReady() :
				walkStep += 5
				walkStep %= 100

			walkCycle(40, walkStep)

			#limitation speed
			#time.sleep(0.1)

			# #if Switch F is up and not receiver is not lost
			# if sbus.get_rx_channels()[15] > 512 and sbus.get_failsafe_status() == 0 :

			# 	#speed from pot S1
			# 	LegSmooth.setAllSpeed( remap(sbus.get_rx_channels()[14], 172, 1811, 5, 500) )

			# 	h = remap(sbus.get_rx_channels()[0], 172, 1811, 0, 80)
			# 	walkCycle(h, walkStep)
			# 	if LegSmooth.allReady() :
			# 		walkStep += remap(sbus.get_rx_channels()[2], 172, 1811, -5, 5)
			# 		walkStep %= 100


			# #if Switch F is down and not receiver is not lost
			# elif sbus.get_rx_channels()[15] < 512 and sbus.get_failsafe_status() == 0 :

			# 	#speed from pot S1
			# 	LegSmooth.setAllSpeed( remap(sbus.get_rx_channels()[14], 172, 1811, 5, 500) )

			# 	h = remap(sbus.get_rx_channels()[0], 172, 1811, 0, 80)
			# 	for leg in LegSmooth:
			# 		leg.position(0,-h,-90+h)

			# #in any other case (receiver lost)
			# else :

			# 	if time.time() - timer0 > 0.5 :
			# 		timer0 = time.time()
			# 		print("No connexion with remote controler")

			# 	LegSmooth.setAllSpeed(50)

			# 	for leg in LegSmooth:
			# 		leg.position(0,0,0)




	except KeyboardInterrupt:
		# sbusUpdateThread_instance.cancel()
		LegSmooth_continue = False
		sbusUpdate_continue = False

		LegSmoothThread_instance.join()
		sbusUpdateThread_instance.join()
		pass

