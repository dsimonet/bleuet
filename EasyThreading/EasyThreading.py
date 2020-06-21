# from : https://python.jpvweb.com/python/mesrecettespython/doku.php?id=function_periodique

##############################################
# THREADING
##############################################

import threading
import time
 
class NewThread(threading.Thread):
 
    def __init__(self, duration, function, args=[], kwargs={}):
        threading.Thread.__init__(self)
        self.duration = duration
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.again = True  # pour permettre l'arret a la demande
 
    def run(self):
        while self.again:
            self.timer = threading.Timer(self.duration, self.function, self.args, self.kwargs)
            self.timer.setDaemon(True)
            self.timer.start()
            self.timer.join()
 
    def stop(self):
        self.again = False  # pour empecher un nouveau lancement de Timer et terminer le thread
        if self.timer.isAlive():
            self.timer.cancel()  # pour terminer une eventuelle attente en cours de Timer


class NewLoopThread(threading.Thread):

    def __init__(self, duration, function, args=[], kwargs={}):
        threading.Thread.__init__(self)
        self.duration = duration
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.again = True  # pour permettre l'arret a la demande
 
    def run(self):
        while self.again:
            self.timer = threading.Timer(self.duration, self.function, self.args, self.kwargs)
            self.timer.setDaemon(True)
            self.timer.start()
            self.timer.join()
 
    def stop(self):
        self.again = False  # pour empecher un nouveau lancement de Timer et terminer le thread
        if self.timer.isAlive():
            self.timer.cancel()  # pour terminer une eventuelle attente en cours de Timer
