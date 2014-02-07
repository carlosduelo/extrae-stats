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

	def printDetail(self):
		if self.idT == 1:
			print ("Main thread " +  
					" (" + 	str(self.timeStart) + ", " + str(self.timeEnd) + ") ")
		else:	
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
