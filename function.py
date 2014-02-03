class Function:
	def __init__(self, _idF):
		self.idF = _idF
		self.timeStamps = {} # idT : (average, time, min, max) 
		self.nCalls = 0
		self.last= []
	def __repr__(self):
		return "Function " + events[self.idF].name + " " + str(self.idF)
	def __str__(self):
		return "Function " + events[self.idF].name + " " + str(self.idF)

	def addTimeStamp(self, tP, tS):
		time = 0
		if tP == 1:
			self.nCalls += 1
			self.last.append((tP, tS))
		else:
			try:
				e = self.last.pop()
				timeB = e[1] 
				idT = e[0] - 1
				if tP:
					self.last.append((tP, tS))
			except IndexError:
				print ("IndexError: adding timeStamp")
				exit(1)
			time = tS - timeB
			if idT in self.timeStamps:
				aT = self.timeStamps[idT][0] + time
				aC = self.timeStamps[idT][1] + 1
				mT = time 
				if mT > self.timeStamps[idT][2]:
					mT = self.timeStamps[idT][2]
				MT = time 
				if MT < self.timeStamps[idT][3]:
					MT = self.timeStamps[idT][3]
				self.timeStamps[idT] = (aT, aC, mT, MT) 
			else:
				self.timeStamps[idT] = (time,1, time, time)
	
	def getCompleteTime(self):
		c = 0
		for i in self.timeStamps:
			c += self.timeStamps[i][0]/self.timeStamps[i][1]
		return c

	def createChart(self):
		print ("Function " + str(events[self.idF])  + " time: " + str(self.getCompleteTime()) + " nanoseconds called: " + str(self.nCalls) + " times")
		if len(self.timeStamps) > 1:
			data = []
			for i in self.timeStamps:
				data.append((i,self.timeStamps[i][0] / self.timeStamps[i][1]))
				print ("\t Step " + str(i) + " time: " + str(self.timeStamps[i][0] /self.timeStamps[i][1]) + " nanoseconds, executed " + str(self.timeStamps[i][1])+ " times.")


