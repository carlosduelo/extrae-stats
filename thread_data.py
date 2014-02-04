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

	def getMinTimeFunction(self, function):
		return 80

	def getMaxTimeFunction(self, function):
		return 150

	def getAverageTimeFunction(self, function):
		return 100

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
