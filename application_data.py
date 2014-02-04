import thread_data as thrd

class Application_Data:
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

	def printListThreads(self):
		for t in self.threads:
			self.threads[t].printDetail()

	def list_functions(self, thread = 0):
		if thread == 0:
			s = set()
			for t in self.threads:
				s = s.union(set(self.threads[t].getFunctions()))
			for e in s:
				print ("Function " + e[1] + " " + str(e[0]))
		else:
			if thread in threads:
				threads[thread].printListFunctions()
			else:
				print ("Please, enter a correct thread id")
		

	def addEventFunction(self, thread, timeStamp, idFunction, name ,value):
		if thread in self.threads:
			t = self.threads[thread]
		else:
			pass
			t = thrd.Thread_Data(thread)
			self.threads[thread] = t
		t.addEvent(timeStamp, idFunction, name, value)

	def addEvent(self, thread, timeStamp, idEvent, name, value):
		pass

	def nCalls_function(self, function):
		l = []
		for t in self.threads:
			l.append(self.threads[t].nCallsFunction(function))
		return l

	def getThreadsID(self):
		return self.threads.keys()

	def getMinTimeFunction(self, function):
		l = []
		for t in self.threads:
			l.append(self.threads[t].getMinTimeFunction(function))
		return l
		
	def getMaxTimeFunction(self, function):
		l = []
		for t in self.threads:
			l.append(self.threads[t].getMaxTimeFunction(function))
		return l
		
	def getAverageTimeFunction(self, function):
		l = []
		for t in self.threads:
			l.append(self.threads[t].getAverageTimeFunction(function))
		return l
		