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

	def getFunctions(self, thread):
		if thread in self.threads:
			return self.threads[thread].getFunctions()
		else:
			print ("Please, enter a correct thread id")
			return []

	def list_functions(self, thread = 0):
		if thread == 0:
			s = set()
			for t in self.threads:
				s = s.union(set(self.threads[t].getFunctions()))
			for e in s:
				print ("Function " + e[1] + " " + str(e[0]))
		else:
			if thread in self.threads:
				self.threads[thread].printListFunctions()
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

	def nCalls_function(self, function, thread):
		if thread == 0:
			l = []
			for t in self.threads:
				l.append(self.threads[t].nCallsFunction(function))
			return l
		elif thread in self.threads:
			return self.threads[thread].getListnCallsIntervalFunction(function)
		else:
			return []
			

	def getThreadsID(self):
		return self.threads.keys()

	def getMinCompleteTimeFunction(self, function):
		l = []
		for t in self.threads:
			l.append(self.threads[t].getMinCompleteTimeFunction(function))
		return l
		
	def getMaxCompleteTimeFunction(self, function):
		l = []
		for t in self.threads:
			l.append(self.threads[t].getMaxCompleteTimeFunction(function))
		return l
		
	def getAverageCompleteTimeFunction(self, function):
		l = []
		for t in self.threads:
			l.append(self.threads[t].getAverageCompleteTimeFunction(function))
		return l
		
	def getMinCompleteTimeThread(self, thread):
		if thread in self.threads:
			return self.threads[thread].getMinCompleteTimeThread()
		else:
			return []
		
	def getMaxCompleteTimeThread(self, thread):
		if thread in self.threads:
			return self.threads[thread].getMaxCompleteTimeThread()
		else:
			return []
		
	def getAverageCompleteTimeThread(self, thread):
		if thread in self.threads:
			return self.threads[thread].getAverageCompleteTimeThread()
		else:
			return []
		
	def getIntervalsFunction(self, thread, function):
		if thread in self.threads:
			return self.threads[thread].getIntervalsFunction(function)
		else:
			return []

	def getAverageIntervalsTimeFunction(self, thread, function):
		if thread in self.threads:
			return self.threads[thread].getAverageIntervalsTimeFunction(function)
		else:
			return []

	def getMinIntervalsTimeFunction(self, thread, function):
		if thread in self.threads:
			return self.threads[thread].getMinIntervalsTimeFunction(function)
		else:
			return []

	def getMaxIntervalsTimeFunction(self, thread, function):
		if thread in self.threads:
			return self.threads[thread].getMaxIntervalsTimeFunction(function)
		else:
			return []

	def getThreadsTimeLine(self):
		l = {}
		for t in self.threads:
			l[t] = self.threads[t].getTimeLine()
		return l
