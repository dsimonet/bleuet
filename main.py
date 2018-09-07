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


def sbusUpdateThreadFunction():
	sbus.update()


def legUpdateThreadFunction():
	LegSmooth.updateAll()

def quitThread():
	sbusThread.stop()
	legThread.stop()

lock = threading.RLock()

#init Thread 
sbus = SBUSReceiver('/dev/ttyS0')

sbusThread = NewThread(0.05, sbusUpdateThreadFunction)
sbusThread.setDaemon(True)
sbusThread.start()


legThread = NewThread(0.000001, legUpdateThreadFunction)
legThread.setDaemon(True)
legThread.start()

# mainTread = NewThread(0.000001, mainThreadFunction)
# mainTread.setDaemon(True)
# mainTread.start()


if __name__ == '__main__':

	timer0 = time.time()
	timer1 = time.time()

	LegSmooth.setAllSpeed(150)

	try :
		while True :

			time.sleep(0.1)
			if sbus.get_rx_channels()[15] > 512 and sbus.get_failsafe_status() == 0 :

				#speed
				LegSmooth.setAllSpeed( remap(sbus.get_rx_channels()[14], 172, 1811, 5, 500) )

				#side
				# if sbus.get_rx_channels()[13] > 1200 :
				# 	LegSmooth.allSetSide(True)
				# elif sbus.get_rx_channels()[13] < 600 :
				# 	LegSmooth.allSetSide(False)


				for leg in LegSmooth :
					a = remap(sbus.get_rx_channels()[0], 172, 1811, -90, 90)
					c = remap(sbus.get_rx_channels()[1], 172, 1811, -90, 90)
					b = remap(sbus.get_rx_channels()[2], 172, 1811, -90, 90)

					leg.position(c,b,a)
				timer0 = time.time()

			else :

				LegSmooth.setAllSpeed(50)
				for leg in LegSmooth:
					leg.position(0,-70,-30)


	except KeyboardInterrupt:
	quitThread()

