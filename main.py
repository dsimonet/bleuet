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
	leg_2 = LegSmooth(3,4,5)
	leg_3 = LegSmooth(6,7,8)
	leg_4 = LegSmooth(9, 10, 11)
	leg_5 = LegSmooth(12, 13, 14)
	# leg_6 = LegSmooth(15, 16 ,5)
	leg_1.mot_phi.reverseMotor()
	leg_2.mot_phi.reverseMotor()
	leg_3.mot_phi.reverseMotor()
	leg_4.mot_phi.reverseMotor()
	leg_5.mot_phi.reverseMotor()
	# leg_6.mot_phi.reverseMotor()

	LegSmooth.setSpeed(1)


	def sbusUpdateThreadFunction():
		with lock :
			t = time.time()
			sbus.update()
			print "sbus ", time.time()-t

	def legUpdateThreadFunction():
		with lock :
			t = time.time()
			LegSmooth.updateAll()
			print "Leg  ", time.time()-t


	#init Thread 
	sbus = SBUSReceiver('/dev/ttyS0')
	sbusThread = NewThread(0.035, sbusUpdateThreadFunction)
	sbusThread.setDaemon(True)
	sbusThread.start()

	legThread = NewThread(0.00001, legUpdateThreadFunction)
	legThread.setDaemon(True)
	legThread.start()

	lock = threading.RLock()
	timer0 = time.time()

	# hexapod init finish
	try:
		while True:
			# print "leg from main", sbus
			with lock :
				if time.time()-timer0 >= 0.0001 and LegSmooth.allReady() :
					#print "leg from thread", sbus.get_rx_channels()[0], "."
					t = time.time()

					z = -remap(sbus.get_rx_channels()[0], 160, 1850, -70,70)
					p = remap(sbus.get_rx_channels()[1], 160, 1850, -70,70)
					for leg in LegSmooth:
						leg.position((t*10)%50, z, z)

					timer0 = time.time()


	except KeyboardInterrupt:
		sys.exit() 
		sbusThread.stop()
		legThread.stop()
		print ""