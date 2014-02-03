#################################################################
######### Functions to parse PRV file ##########################
#################################################################

class Application:
	def __init__(self):
		self.eventID = 0 
		self.timeStart = 0
		self.timeEnd = 0

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
	


class ParserPRV:
	def __init__(self, _file_name, _parserPCF):
		self.file_name = _file_name
		self.parserPCF = _parserPCF
		self.app		= Application()

	def parseFile(self):
		print ("Parsing " + self.file_name + ".....")

		f = open(self.file_name)

		line = f.readline()

		if "#Paraver" in line[0:8]:
			line = f.readline()
		else:
			print ("Error no Paraver file")
			exit(1)

		while line :
			elements = line.split(":")

			try:

				if int(elements[0]) == 1:
					pass
				elif int(elements[0]) == 2:
					if int(elements[2]) != 1:
						print ("Error, different apps? " + line)
					process = int(elements[3])
					thread = int(elements[4])

					#if not (thread in threads.keys()):
					#	t = Thread(thread)
					#	threads[thread] = t

					#t = threads[thread]

					timeStamp = int(elements[5])
					for i in range(6,len(elements), 2):
						e = int(elements[i])
						if self.parserPCF.isAppEvent(e):
							v = int(elements[i+1])
							if v:
								self.app.addStart(timeStamp)
							else:
								self.app.addEnd(timeStamp)

						#elif e in valid_events:
						#	v = int(elements[i+1])
							#print ("Thread " + str(thread) + " timeStamp " + str(timeStamp) + " event " + str(e) + " value " + str(v))
						#	t.addEvent(timeStamp, e, v)


				elif int(elements[0]) == 3:
					pass
				elif elements[0] == "c":
					pass
				else:
					print ("Error parsing line " + line)
					exit(1)
					
			except ValueError:
				print ("Error parsing line " + line)
				
			line = f.readline()

	def	printAppTimes(self):
		self.app.printTime()

#################################################################
#################################################################

