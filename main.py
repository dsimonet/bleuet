#!/usr/bin/env python
#-*- coding: utf-8 -*-




##############################################
# MAIN
##############################################




# excuted if this doc is not imported
# for testing purpose only
if __name__ == '__main__':

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
	# leg_6 = LegSmooth(15, 16 ,5)
	leg_1.mot_phi.reverseMotor()
	leg_2.mot_phi.reverseMotor()
	leg_3.mot_phi.reverseMotor()
	leg_4.mot_phi.reverseMotor()
	leg_5.mot_phi.reverseMotor()
	leg_6.mot_phi.reverseMotor()
	# leg_6.mot_phi.reverseMotor()

	LegSmooth.setSpeed(2)

	# def sbusUpdateThreadFunction():

	# 	sbus.update()

	# def legUpdateThreadFunction():

	# 	LegSmooth.updateAll()


	#init Thread 
	sbus = SBUSReceiver('/dev/ttyS0')
	# sbusThread = NewThread(0.035, sbusUpdateThreadFunction)
	# sbusThread.setDaemon(True)
	# sbusThread.start()

	# legThread = NewThread(0.00001, legUpdateThreadFunction)
	# legThread.setDaemon(True)
	# legThread.start()

	timerSbus = time.time()
	timerLeg = time.time()
	timerMain = time.time()
	# hexapod init finish
	try:
		while True:
			if time.time()-timerMain >= 0.05 :
				#print "leg from thread", sbus.get_rx_channels()[0], "."
				z = -remap(sbus.get_rx_channels()[0], 160, 1850, -70,70)
				p = remap(sbus.get_rx_channels()[1], 160, 1850, -70,70)
				for leg in LegSmooth:
					leg_1.position(p, z, z)
					time.sleep(0.001)

			if time.time()-timerSbus >= 0.035 :
				sbus.update()

			if time.time() - timerLeg >= 0.1:
				LegSmooth.updateAll()
				while LegSmooth.allReady():
					pass


	except KeyboardInterrupt:
		# sbusThread.stop()
		# legThread.stop()
		print ""