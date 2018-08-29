#!/usr/bin/env python
#-*- coding: utf-8 -*-




##############################################
# MAIN
##############################################




import time
import random
from hexa_pi import *
from sbus_driver_python import *
from EasyThreading import *
	

# init leg
leg_1 = LegSmooth(24,25,26)
leg_2 = LegSmooth(20,21,22)
leg_3 = LegSmooth(16,17,18)
leg_4 = LegSmooth(8, 9, 10)
leg_5 = LegSmooth(4, 5, 6)
leg_6 = LegSmooth(0, 1, 2)

LegSmooth.setSpeed(1)

lock = threading.RLock()

def sbusUpdateThreadFunction():
	with lock :
		t = time.time()
		sbus.update()
		print "sbus :", time.time() - t

def legUpdateThreadFunction():
	with lock :
		t = time.time()
		LegSmooth.updateAll()
		print "leg  :", time.time() - t

def quitThread():
	sbusThread.stop()
	legThread.stop()

#init Thread 
sbus = SBUSReceiver('/dev/ttyS0')
sbusThread = NewThread(0.035, sbusUpdateThreadFunction)
sbusThread.setDaemon(True)
sbusThread.start()

legThread = NewThread(0.00001, legUpdateThreadFunction)
legThread.setDaemon(True)
legThread.start()


# hexapod init finish
	
timerMain = time.time()

try:
	while True:
		if time.time() - timerMain >= 0.001 :
			with lock :
				t = time.time()
				if sbus.get_rx_channels()[15] > 512:

					z = -remap(sbus.get_rx_channels()[0], 160, 1850, -90,90)
					p = remap(sbus.get_rx_channels()[1], 160, 1850, -90,90)

					for leg in LegSmooth:
						leg.position(p, z, z)
				else :

					for leg in LegSmooth:
						leg.position(0,0,0)

				print "main :", time.time() - t

except KeyboardInterrupt:
	quitThread()



