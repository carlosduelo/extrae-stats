import thread as thrd

class Application:
	def __init__(self):
		self.eventID = 0 
		self.timeStart = 0
		self.timeEnd = 0
		self.threads = {}

	def setEventID(self, _eventID):
		self.eventID = _eventID

	def isApplicationEvent(self, _eventID):
		return self.eventID == _eventID

	def addStart(self, t):
		self.timeStart = t

	def addEnd(self, t):
		self.timeEnd = t

	def getCompleteTime(self):
		return self.timeEnd - self.timeStart

	def printTime(self):
		print ("Application time: " + str(self.getCompleteTime())+ " nanoseconds")

	def addEventFunction(self, thread, timeStamp, idFunction, value):
		if thread in self.threads:
			t = self.threads[thread]
		else:
			t = thrd.Thread(thread)
			self.threads[thread] = t

	def addEvent(self, thread, timeStamp, idEvent, value):
		pass

