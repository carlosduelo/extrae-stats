import function_data as func

class Thread_Data:
	def __init__(self, _idT):
		self.idT = _idT
		self.functions = {}
		self.timeStart = -1
		self.timeEnd = 0
	def __repr__(self):
		return "Thread " + str(self.idT)
	def __str__(self):
		return "Thread " + str(self.idT)

	def getTimeLine(self):
		return (self.timeStart, self.timeEnd)

	def printListFunctions(self):
		for i in self.functions:
			print (self.functions[i])
	
	def getFunctions(self):
		f = []
		for i in self.functions:
			f.append((self.functions[i].idF, self.functions[i].name))
		return f
			
	def nCallsFunction(self, func):
		if func in self.functions:
			return self.functions[func].nCalls
		else:
			return 0

	def getListnCallsIntervalFunction(self, function):
		l = []
		if function in self.functions:
			l = self.functions[function].getListnCallsInterval()
		return l

	def printDetail(self):
		print ("Thread " + str(self.idT) + 
				" (" + 	str(self.timeStart) + ", " + str(self.timeEnd) + ") ")

	def getMinCompleteTimeFunction(self, function):
		if function in self.functions:
			return self.functions[function].getCompleteMinTime()
		else:
			return 0

	def getMaxCompleteTimeFunction(self, function):
		if function in self.functions:
			return self.functions[function].getCompleteMaxTime()
		else:
			return 0

	def getAverageCompleteTimeFunction(self, function):
		if function in self.functions:
			return self.functions[function].getCompleteAverageTime()
		else:
			return 0

	def getIntervalsFunction(self, function):
		if function in self.functions:
			return self.functions[function].getIntervals()
		else:
			return []

	def getAverageIntervalsTimeFunction(self, function):
		if function in self.functions:
			return self.functions[function].getAverageIntervalsTime()
		else:
			return []

	def getMinIntervalsTimeFunction(self, function):
		if function in self.functions:
			return self.functions[function].getMinIntervalsTime()
		else:
			return []

	def getMaxIntervalsTimeFunction(self, function):
		if function in self.functions:
			return self.functions[function].getMaxIntervalsTime()
		else:
			return []

	def getMinCompleteTimeThread(self):
		l = []
		for f in self.functions:
			l.append(self.functions[f].getCompleteMinTime())
		return l

	def getMaxCompleteTimeThread(self):
		l = []
		for f in self.functions:
			l.append(self.functions[f].getCompleteMaxTime())
		return l

	def getAverageCompleteTimeThread(self):
		l = []
		for f in self.functions:
			l.append(self.functions[f].getCompleteAverageTime())
		return l

	def addEvent(self, timeStamp, idF, name, value):
		if self.timeStart == -1:
			self.timeStart = timeStamp
		self.timeEnd = timeStamp
		if idF in self.functions:
			self.functions[idF].addTimeStamp(value, timeStamp)
		else:
			f = func.Function_Data(idF, name)
			f.addTimeStamp(value, timeStamp)
			self.functions[idF] = f
