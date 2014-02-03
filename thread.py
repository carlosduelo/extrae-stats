class Thread:
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

	def addEvent(self, timeStamp, idF, value):
		if self.timeStart == -1:
			self.timeStart = timeStamp
		self.timeEnd = timeStamp
		if idF in self.functions:
			self.functions[idF].addTimeStamp(value, timeStamp)
		else:
			f = Function(idF)
			f.addTimeStamp(value, timeStamp)
			self.functions[idF] = f

	def createCharts(self):
		print("Thread " + str(self.idT))
		data = []
		for f in self.functions:
			data.append((self.functions[f].idF, self.functions[f].getCompleteTime()))
			self.functions[f].createChart()

		#matplotlib.pyplot.figure()
		#N = len(data)
		#x = numpy.arange(1, N + 1)
		#y = [ num for (s, num) in data ]
		#labels = [ s for (s, num) in data ]
		#width = 1
		#r1 = matplotlib.pyplot.bar( x, y, width, color="y" )
		#matplotlib.pyplot.title( "Functions on thread " + str(self.idT))
		#matplotlib.pyplot.ylabel( 'Nanoseconds' )
		#matplotlib.pyplot.xticks(x, labels )
		#matplotlib.pyplot.savefig("thread"+str(self.idT)+".png")
