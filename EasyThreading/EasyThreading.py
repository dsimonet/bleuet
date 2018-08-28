# from : https://python.jpvweb.com/python/mesrecettespython/doku.php?id=fonction_periodique

##############################################
# THREADING
##############################################

import threading
import time
 
class NewThread(threading.Thread):
 
    def __init__(self, duree, fonction, args=[], kwargs={}):
        threading.Thread.__init__(self)
        self.duree = duree
        self.fonction = fonction
        self.args = args
        self.kwargs = kwargs
        self.encore = True  # pour permettre l'arret a la demande

        time.sleep(0.1)
 
    def run(self):
        while self.encore:
            self.timer = threading.Timer(self.duree, self.fonction, self.args, self.kwargs)
            self.timer.setDaemon(True)
            self.timer.start()
            self.timer.join()
 
    def stop(self):
        self.encore = False  # pour empecher un nouveau lancement de Timer et terminer le thread
        if self.timer.isAlive():
            self.timer.cancel()  # pour terminer une eventuelle attente en cours de Timer

        time.sleep(0.1)





"""

t =  Intervallometre(duree, affiche, ["toto"], {'x':"titi", 'y':"tata"})
t.setDaemon(True)
t.start()
 
time.sleep(5.1)
t.stop()
 
t2 =  Intervallometre(duree, affiche2, ["toto2"], {'x':"titi", 'y':"tata"})
t2.setDaemon(True)
t2.start()
 
time.sleep(5.1)
t2.stop()
 
t3 =  Intervallometre(duree, affiche3, ["toto3"], {'x':"titi", 'y':"tata"})
t3.setDaemon(True)
t3.start()
 
time.sleep(5.1)
t3.stop()

"""