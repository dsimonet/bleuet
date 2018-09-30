#!/usr/bin/env python
#-*- coding: utf-8 -*-




##############################################
# MAIN
##############################################



# from __future__ import division

import time
import random
from hexa_pi import *
from sbus_driver_python import *
from EasyThreading import *

	

# init leg
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

#create simples functions for threading and exit threading
lock = threading.RLock()

def sbusUpdateThreadFunction():
	sbus.update()

def legUpdateThreadFunction():
	LegSmooth.updateAll()

def quitThread():
	sbusThread.stop()
	legThread.stop()


#init Thread 
sbusThread = NewThread(0.05, sbusUpdateThreadFunction)
sbusThread.setDaemon(True)
sbusThread.start()

legThread = NewThread(0.00001, legUpdateThreadFunction)
legThread.setDaemon(True)
legThread.start()


def walkCycle(h, v):

	majorStep = 100.0/4.0
	subStep =  majorStep/3.0
	microStep = remap((v%majorStep)%subStep, 0, subStep, 0, 1)


	upAPosition = 10
	upBPosition = -80
	downAPosition = -h
	downBPosition = -90+h
	phiFront = 20
	phiBack = -20

	#move odd leg
	if v < majorStep :
		if v < subStep :	#up
			leg_1.position(phiBack,upAPosition*microStep,upBPosition*microStep)
			leg_3.position(phiBack,upAPosition*microStep,upBPosition*microStep)
			leg_5.position(-phiBack,upAPosition*microStep,upBPosition*microStep)
		elif v < subStep*2 :	#front
			leg_1.position(phiFront,upAPosition,upBPosition)
			leg_3.position(phiFront,upAPosition,upBPosition)
			leg_5.position(-phiFront,upAPosition,upBPosition)
		elif v < subStep*3 :	#down
			leg_1.position(phiFront,downAPosition,downBPosition)
			leg_3.position(phiFront,downAPosition,downBPosition)
			leg_5.position(-phiFront,downAPosition,downBPosition)
			
		#redefining other legs in any case	
		leg_2.position(phiFront,downAPosition,downBPosition)
		leg_4.position(-phiFront,downAPosition,downBPosition)
		leg_6.position(-phiFront,downAPosition,downBPosition)

	#move body front
	elif v > majorStep and v < majorStep*2:
		leg_1.position(phiBack,downAPosition,downBPosition)
		leg_2.position(phiBack,downAPosition,downBPosition)
		leg_3.position(phiBack,downAPosition,downBPosition)
		leg_4.position(-phiBack,downAPosition,downBPosition)
		leg_5.position(-phiBack,downAPosition,downBPosition)
		leg_6.position(-phiBack,downAPosition,downBPosition)

	#move even leg
	elif v > majorStep*2 and v < majorStep * 3:
		if v < majorStep*2 + subStep :	#up
			leg_2.position(-phiFront,upAPosition,upBPosition)
			leg_4.position(phiFront,upAPosition,upBPosition)
			leg_6.position(phiFront,upAPosition,upBPosition)
		elif v < majorStep*2 + subStep*2 :	#front
			leg_2.position(-phiBack,upAPosition,upBPosition)
			leg_4.position(phiBack,upAPosition,upBPosition)
			leg_6.position(phiBack,upAPosition,upBPosition)
		elif v < majorStep*2 + subStep*3 :	#down
			leg_2.position(-phiBack,downAPosition,downBPosition)
			leg_4.position(phiBack,downAPosition,downBPosition)
			leg_6.position(phiBack,downAPosition,downBPosition)
			
		#redefining other legs in any case	
		leg_1.position(phiBack,downAPosition,downBPosition)
		leg_3.position(phiBack,downAPosition,downBPosition)
		leg_5.position(-phiBack,downAPosition,downBPosition)

	#move body front
	elif v > majorStep*3 :
		leg_1.position(phiBack,downAPosition,downBPosition)
		leg_2.position(phiBack,downAPosition,downBPosition)
		leg_3.position(phiBack,downAPosition,downBPosition)
		leg_4.position(-phiBack,downAPosition,downBPosition)
		leg_5.position(-phiBack,downAPosition,downBPosition)
		leg_6.position(-phiBack,downAPosition,downBPosition)





if __name__ == '__main__':

	timer0 = time.time()
	timer1 = time.time()

	LegSmooth.setAllSpeed(500)

	walkStep = 0

	try :
		while True :

			#limitation speed
			time.sleep(0.1)

			#if Switch F is up and not receiver is not lost
			if sbus.get_rx_channels()[15] > 512 and sbus.get_failsafe_status() == 0 :

				#speed from pot S1
				LegSmooth.setAllSpeed( remap(sbus.get_rx_channels()[14], 172, 1811, 5, 500) )

				h = remap(sbus.get_rx_channels()[0], 172, 1811, 0, 80)
				walkCycle(h, walkStep)
				if LegSmooth.allReady() :
					walkStep += remap(sbus.get_rx_channels()[2], 172, 1811, -5, 5)
					walkStep %= 100


			#if Switch F is down and not receiver is not lost
			elif sbus.get_rx_channels()[15] < 512 and sbus.get_failsafe_status() == 0 :

				#speed from pot S1
				LegSmooth.setAllSpeed( remap(sbus.get_rx_channels()[14], 172, 1811, 5, 500) )


				h = remap(sbus.get_rx_channels()[0], 172, 1811, 0, 80)
				for leg in LegSmooth:
					leg.position(0,-h,-90+h)

			#in any other case (receiver lost)
			else :
				LegSmooth.setAllSpeed(50)

				for leg in LegSmooth:
					leg.position(0,0,0)


	except KeyboardInterrupt:
		quitThread()

