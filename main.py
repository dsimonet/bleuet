#!/usr/bin/env python
#-*- coding: utf-8 -*-

import time
import random
from body import *

##############################################
# MAIN
##############################################


body = body()

body.Down()
body.Up()
body.Down()
body.Stand()



"""
#on init les objet patte avec l'assignation du bus (pas encore codé) et la pin ou est branché le servo (x3)
patte_0 = Patte(0,0,1,2)
patte_1 = Patte(0,4,5,6)
patte_2 = Patte(0,8,9,10)

Patte.speed(16)

#on init le system de mise à jour des pattes

t =  Intervallometre(0.008, Patte.updateAll)
t.setDaemon(True)
t.start()


while 1 :
	Patte.allPosition(50,90,0)
	Patte.waitUntilFinish()

	Patte.allPosition(50,80,10)
	Patte.waitUntilFinish()

	Patte.allPosition(50,90,0)
	Patte.waitUntilFinish()

	Patte.allPosition(50,5,70)
	Patte.waitUntilFinish()

#on stop le Thread
#et on range tout
Patte.waitUntilFinish()
Patte.speed(16)
for p in Patte._registry :
	p.standPosition()
Patte.waitUntilFinish()

t.stop()
time.sleep(0.2)

"""