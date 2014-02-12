import functools

class Function_Data:
	def __init__(self, _idF, _name):
		self.idF = _idF
		self.name = _name
		self.timeStamps = {} # { idT : ([elapsed_time], n_times, min_elapsed_time, max_elapsed_time) }
		self.completeStamp = [] # [elapsed_time]
		self.minCompleteStamp = 0
		self.maxCompleteStamp = 0
		self.nCalls = 0
		self.lastT = []
		self.lastC = []
	def __repr__(self):
		return "Function " + self.name + " " + str(self.idF)
	def __str__(self):
		return "Function " + self.name + " " + str(self.idF)
		
	def getListnCallsInterval(self):
		l = []
		for i in self.timeStamps:
			l.append(self.timeStamps[i][1])
		return l

	def addTimeStamp(self, tP, tS):
		time = 0
		if tP == 1:
			self.nCalls += 1
			self.lastT.append((tP, tS))
			self.lastC.append(tS)
		else:
			# End function
			if tP == 0:
				try:
					t = self.lastC.pop()
				except IndexError:
					print ("IndexError: adding timeStamp in function " + str(self.idF) + " " + self.name + " " +  str(tP) + " " + str(tS) + "\n Discarded")
					return
				timeC = tS - t
				self.completeStamp.append(timeC)
				if self.minCompleteStamp == 0:
					self.minCompleteStamp = timeC
					self.maxCompleteStamp= timeC
				else:
					if timeC < self.minCompleteStamp : self.minCompleteStamp = timeC
					if timeC > self.maxCompleteStamp : self.maxCompleteStamp = timeC
				
			try:
				e = self.lastT.pop()
				timeB = e[1] 
				idT = e[0] - 1
				if tP:
					self.lastT.append((tP, tS))
			except IndexError:
				print ("IndexError: adding timeStamp")
				exit(1)
			time = tS - timeB
			if idT in self.timeStamps:
				aT = self.timeStamps[idT][0]
				aT.append(time)
				aC = self.timeStamps[idT][1] + 1
				mT = time 
				if mT > self.timeStamps[idT][2]:
					mT = self.timeStamps[idT][2]
				MT = time 
				if MT < self.timeStamps[idT][3]:
					MT = self.timeStamps[idT][3]
				self.timeStamps[idT] = (aT, aC, mT, MT) 
			else:
				self.timeStamps[idT] = ([time], 1, time, time)
	
	def getCompleteAverageTime(self):
		return functools.reduce(lambda x, y : x + y, self.completeStamp) / len(self.completeStamp) 

	def getCompleteMinTime(self):
		return self.minCompleteStamp

	def getCompleteMaxTime(self):
		return self.maxCompleteStamp

	def getIntervals(self):
		return self.timeStamps.keys()

	def getAverageIntervalsTime(self):
		l = []
		for t in self.timeStamps:
			l.append(functools.reduce(lambda x, y : x + y, self.timeStamps[t][0]) / len(self.timeStamps[t][0]))
		return l

	def getMinIntervalsTime(self):
		l = []
		for t in self.timeStamps:
			l.append(self.timeStamps[t][2])
		return l

	def getMaxIntervalsTime(self):
		l = []
		for t in self.timeStamps:
			l.append(self.timeStamps[t][3])
		return l
