from threading import Thread
from leg import Leg
import ease

class LegSmooth(Leg) :


	def __init__(self, _phi, _A, _B) :
		Leg.__init__(self, _phi, _A, _B)

		#veleurs des positions des moteurs 
		# 50 5 et 70 pour un stand
		self.phi = 50
		self.a = 5
		self.b = 70

		self.phiFrom = self.phi
		self.aFrom = self.a
		self.bFrom = self.b

		self.phiTo = self.phi
		self.aTo = self.a
		self.bTo = self.b 	





"""		
	@staticmethod
	def speed(v):
		Leg._duration = v

	@staticmethod
	def allReady() :
		for i in Leg._registry :
			if i.ready :
				continue
			else:
				return False
		return True


	@staticmethod
	def waitUntilFinish():
		while not Leg.allReady() :
			pass
	

	def updateSoft(self):

		#on calcul la position actuel avec une fonction ease
		#ease(t, b, c, d)
		# t is the current time (or position) of the tween.
		# b is the beginning value of the property.
		# c is the change between the beginning and destination value of the property.
		# d is the total time of the tween.
		self.phi = ease.easeInOutQuad(float(self._counter), self.phiFrom, self.phiTo-self.phiFrom, float(self._duration) )
		self.a = ease.easeInOutQuad(float(self._counter), self.aFrom, self.aTo-self.aFrom, float(self._duration) )
		self.b = ease.easeInOutQuad(float(self._counter), self.bFrom, self.bTo-self.bFrom, float(self._duration) )

		# on update le counter qui nous laisse une trace de notre position sur la courbe de ease

		if self._counter < self._duration :
			self._counter += 1
			self.ready = False
		else:
			self.ready = True

		#On fait bouger les moteurs en fonction des nouvelles valeurs calculé
		self.move(self.phi, self.a, self.b)
	
"""