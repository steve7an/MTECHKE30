# Fall detector Person class
#
# Kim Salmi, kim.salmi(at)iki(dot)fi
# http://tunn.us/arduino/falldetector.php
# License: GPLv3
import settings
import numpy as np

class Person(object):
	"""Person"""
	count = 0

	def __init__(self, x, y, w, h, movementMaximum, movementMinimum, movementTime):
		self.settings = settings.Settings()
		self.debug = self.settings.debug
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.movementTime = movementTime
		self.movementMaximum = movementMaximum
		self.movementMinimum = movementMinimum
		self.lastmoveTime = 0
		self.alerts = [0,0]
		self.alarmReported = 0
		self.lastseenTime = 0
		self.remove = 0
		self.w_ratio = self.settings.person_w_ratio
		self.h_ratio = self.settings.person_h_ratio
		self.arr_h = []
		self.arr_w = []
		self.keep_last_count = self.settings.person_keep_last_count

		Person.count += 1
		if Person.count > 1000:
			Person.count = 0
		self.id = Person.count

	def samePerson(self, x, y, w, h):
		same = 0
		if x+self.movementMaximum > self.x and x-self.movementMaximum < self.x:
			if y+self.movementMaximum > self.y and y-self.movementMaximum < self.y:
				same = 1
		return same

	def popFIFO(self, arr):
		arr.reverse()
		arr.pop()
		arr.reverse()

	def compareMovement(self, w, h):
		#print ("Length of arr w {0}".format(len(self.arr_w)))
		
		self.arr_w.append(self.w)
		self.arr_h.append(self.h)

		if len(self.arr_w) == self.keep_last_count:
			self.popFIFO(self.arr_w)
		if len(self.arr_h) == self.keep_last_count:
			self.popFIFO(self.arr_h)
		
		prev_w_mean = np.mean(self.arr_w)
		prev_h_mean = np.mean(self.arr_h)
		cur_w_ratio = w/prev_w_mean
		cur_h_ratio = prev_h_mean/h
		if cur_w_ratio >= self.w_ratio and cur_h_ratio >= self.h_ratio:
			self.alerts[0] = 1

		if self.debug:
			print ("W {0} and Self W {1}, prev mean {2}, div {3} vs w ratio {4}".format(w, 
				self.w, prev_w_mean, cur_w_ratio, self.w_ratio))
			print ("H {0} and Self H {1}, prev mean {2}, div {3} vs H ratio {4}".format(h, 
				self.h, prev_h_mean, cur_h_ratio, self.h_ratio))


	def editPerson(self, x, y, w, h):
		if abs(x-self.x) > self.movementMinimum or abs(y-self.y) > \
		self.movementMinimum or abs(w-self.w) > self.movementMinimum or \
		abs(h-self.h) > self.movementMinimum:
			self.lastmoveTime = 0
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.lastseenTime = 0

	def getId(self):
		return self.id

	def tick(self):
		self.lastmoveTime += 1
		self.lastseenTime += 1

		if self.lastmoveTime > self.movementTime:
			self.alerts[1] = 1

		if self.lastseenTime > 4: # how many frames ago last seen
			self.remove = 1
			
	def getAlert(self):
		return self.alerts

	def getRemove(self):
		return self.remove


class Persons:
	def __init__(self, movementMaximum, movementMinimum, movementTime):
		self.persons = []
		self.movementMaximum = movementMaximum
		self.movementMinimum = movementMinimum
		self.movementTime = movementTime
		Person.count = 0
		self.settings = settings.Settings()
		self.debug = self.settings.debug

	def addPerson(self, x, y, w, h):
		person = self.familiarPerson(x, y, w, h)
		if person:
			person.compareMovement(w, h)
			person.editPerson(x, y, w, h)
			return person
		else:
			person = Person(x ,y ,w ,h , self.movementMaximum, 
				self.movementMinimum, self.movementTime)
			self.persons.append(person)
			return person
		
	def familiarPerson(self, x, y, w, h):
		for person in self.persons:
			if person.samePerson(x, y, w, h):
				return person
		return None

	def tick(self):
		for person in self.persons:
			person.tick()
			if person.getRemove():
				self.persons.remove(person)
