#!/usr/bin/env python
#-*- coding: utf-8 -*-




##############################################
# MAIN
##############################################




import time
import sys
import random
from hexa_pi import *
from sbus_driver_python import *
from EasyThreading import *
	

leg_1 = LegSmooth(24,25,26)
leg_2 = LegSmooth(20,21,22)
leg_3 = LegSmooth(16,17,18)
leg_4 = LegSmooth(8, 9, 10)
leg_5 = LegSmooth(4, 5, 6)
leg_6 = LegSmooth(0, 1, 2)

sbus = SBUSReceiver('/dev/ttyS0')



if __name__ == '__main__':

	timer0 = time.time()
	timer1 = time.time()

	LegSmooth.setAllSpeed(150)

	try :
		while True :

			sbus.update()

			if sbus.get_rx_channels()[15] > 512 and sbus.get_failsafe_status() == 0 :

				#speed
				LegSmooth.setAllSpeed( remap(sbus.get_rx_channels()[14], 172, 1811, 5, 500) )

				#side
				if sbus.get_rx_channels()[13] > 1200 :
					LegSmooth.allSetSide(True)
				elif sbus.get_rx_channels()[13] < 600 :
					LegSmooth.allSetSide(False)


				for leg in LegSmooth :
					a = remap(sbus.get_rx_channels()[0], 172, 1811, -90, 90)
					c = remap(sbus.get_rx_channels()[1], 172, 1811, -90, 90)
					b = remap(sbus.get_rx_channels()[2], 172, 1811, -90, 90)

					leg.position(c,b,a)
				LegSmooth.positionSync()
				LegSmooth.updateAll()
				timer0 = time.time()

			else :

				LegSmooth.setAllSpeed(20)
				for leg in LegSmooth:
					leg.position(0,70,30)

			LegSmooth.updateAll()

	except KeyboardInterrupt:
		pass
