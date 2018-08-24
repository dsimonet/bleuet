#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import random


##############################################
# MAIN
##############################################




# excuted if this doc is not imported
# for testing purpose only
if __name__ == '__main__':

	from hexa_pi import *
	from sbus_driver_python import *


	sbus = SBUSReceiver('/dev/ttyS0')

	# init leg

	leg_1 = LegSmooth(0,1,2)
	leg_1.mot_phi.reverseMotor()


	#init Thread LEG

	LegSmooth.setSpeed(4)
	LegSmooth.startThread()
	LegSmooth.waitUntilFinish()
	
	#make leg move to a position in x y z global (hexapod local)

	time.sleep(1)

	timer1 = time.time()
	timer2 = time.time()+0.1

	while True:


		if sbus.get_rx_channels()[4] >= 512 and sbus.isSync:
			a = remap(sbus.get_rx_channels()[0], 160, 1850, 90,-90)
			b = a
			phi = remap(sbus.get_rx_channels()[1], 160, 1850, -90,90) 
			
			leg_1.position(phi,a,b)


		if time.time() - timer1 > 0.01:
			sbus.get_new_data()
			timer1 = time.time()

		if time.time() - timer2 > 0.2:
			#print a,b, phi
			timer2 = time.time()



	# leg_2.position(-85,0,60)
	# leg_3.position(85,-85,60)
	# leg_4.position(85,0,60)
	
	LegIK.waitUntilFinish()

	#Clean end	
	time.sleep(0.5)
	LegSmooth.closeThread()
	time.sleep(0.2)
	#LegIK.offAllLegSmooth()
