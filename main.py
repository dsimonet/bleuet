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
	from EasyThreading import *


	# init leg
	leg_1 = LegIK(0,1,2, 30)
	leg_1.mot_phi.reverseMotor()
	LegSmooth.setSpeed(2)


	#init Thread 
	sbus = SBUSReceiver('/dev/ttyS0')
	sbusThread = NewThread(0.08, sbus.get_new_data)
	sbusThread.setDaemon(True)
	sbusThread.start()

	legThread = NewThread(0.0001, LegSmooth.updateSoftAll)
	legThread.setDaemon(True)
	legThread.start()
	time.sleep(0.5)

	# hexapod init finish

	timer1 = time.time()
	timer2 = time.time()+0.1

	while True:

		z = remap(sbus.get_rx_channels()[0], 160, 1850, 0,40)
		x = remap(sbus.get_rx_channels()[3], 160, 1850, 0,50) 
		y = remap(sbus.get_rx_channels()[2], 160, 1850, 0,50) 

		if time.time() - timer1 > 0.001:
			leg_1.position(z,z,z)
			timer1 = time.time()

		if time.time() - timer2 > 0.02:
			print z
			timer2 = time.time()


