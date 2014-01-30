#!/usr/bin/python

import sys
import numpy 
import matplotlib.pyplot 

print ("Creating statistics....")

# File names
PRV="NOT FOUND"
PCF="NOT FOUND"
FUNC="NOT FOUND"

class Event:
	def __init__(self, _idE, _name):
		self.idE = _idE
		self.name = _name
	def __repr__(self):
		return self.name + " " + str(self.idE)
	def __str__(self):
		return self.name + " " + str(self.idE)

class Function:
	def __init__(self, _idF):
		self.idF = _idF
		self.timeStamps = {} 
		self.nCalls = 0
		self.last= []
	def __repr__(self):
		return "Function " + str(self.idF)
	def __str__(self):
		return "Function " + str(self.idF)

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
				self.timeStamps[idT] = (aT, aC) 
			else:
				self.timeStamps[idT] = (time,1)
	
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

class Thread:
	def __init__(self, _idT):
		self.idT = _idT
		self.functions = {}
	def __repr__(self):
		return "Thread " + str(self.idT)
	def __str__(self):
		return "Thread " + str(self.idT)

	def addEvent(self, timeStamp, idF, value):
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

		#N = len(data)
		#x = numpy.arange(1, N + 1)
		#y = [ num for (s, num) in data ]
		#labels = [ s for (s, num) in data ]
		#width = 1
		#r1 = matplotlib.pyplot.bar( x, y, width, color="y" )
		#matplotlib.pyplot.ylabel( 'Intensity' )
		#matplotlib.pyplot.xticks(x, labels )
		#matplotlib.pyplot.show()

# Global variables
states = {}
events = {} 
valid_events = []
threads ={}

#################################################################
######### Functions to parse PCF file ##########################
#################################################################

def parsePRV():
	print ("Parsing " + PRV + ".....")

	f = open(PRV)

	state = -1
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

				if not (thread in threads.keys()):
					t = Thread(thread)
					threads[thread] = t

				t = threads[thread]

				timeStamp = int(elements[5])
				for i in range(6,len(elements), 2):
					e = int(elements[i])
					if e in valid_events:
						v = int(elements[i+1])
						#print ("Thread " + str(thread) + " timeStamp " + str(timeStamp) + " event " + str(e) + " value " + str(v))
						t.addEvent(timeStamp, e, v)


			elif int(elements[0]) == 3:
				pass
			else:
				print ("Error parsing line " + line)
				exit(1)
				
		except ValueError:
			print ("Error parsing line " + line)
			
		line = f.readline()


#################################################################
#################################################################

#################################################################
######### Functions to parse FUNC file ##########################
#################################################################

def parseFUNC():
	print ("Parsing " + FUNC + ".....")

	f = open(FUNC)
	line = f.readline()

	if "#Functions" in line[0:10]:
		line = f.readline()
	else:
		print ("Error no Functions file")
		exit(1)

	while line :
		try:
			valid_events.append(int(line))
		except ValueError:
			print ("Error parsing line: " + line)
			exit(1)
		line = f.readline()


#################################################################
#################################################################


#################################################################
######### Functions to parse PCF file ##########################
#################################################################

def parsePCF_DEFAULT_OPTIONS(line):
	if "LEVEL" in line[0:5]:
		pass
	elif "UNITS" in line[0:5]:
		pass
	elif "LOOK_BACK" in line[0:9]:
		pass
	elif "SPEED" in line[0:5]:
		pass
	elif "FLAG_ICONS" in line[0:10]:
		pass
	elif "NUM_OF_STATE_COLORS" in line[0:19]:
		pass
	elif "YMAX_SCALE" in line[0:10]:
		pass
	elif "\n" in line[0]:
		pass
	else:
		print ("Error parsing line: " + line)

def parsePCF_DEFAULT_SEMANTIC(line):
	if "THREAD_FUNC" in line[0:11]:
		pass
	elif "\n" in line[0]:
		pass
	else:
		print ("Error parsing line: " + line)

def parsePCF_STATES_COLOR(line):
	if "THREAD_FUNC" in line[0:11]:
		pass
	elif "\n" in line[0]:
		pass

def parsePCF_STATES(line):
	if "\n" in line[0]:
		pass
	else:
		elements = line.split()
		try:
			s = int(elements[0])
			states[elements[1]] = s
		except ValueError:
			print ("Error parsing line " + line)
		
def parsePCF_EVENT_TYPE(line, f):
	if "\n" in line[0]:
		pass
	elif "VALUES" in line[0:6]:
		l = f.readline()
		while l != "\n":
			l = f.readline()
	else:
		elements = line.split()
		try:
			e = int(elements[1])
			n = "".join(elements[2:])
			events[e] = Event(e, n)
		except ValueError:
			print ("Error parsing line " + line)

def parsePCF_GRADIENT_COLOR(line):
	if "\n" in line[0]:
		pass
	else:
		elements = line.split(" ")

def parsePCF_GRADIENT_NAMES(line):
	if "\n" in line[0]:
		pass
	else:
		elements = line.split(" ")

# STATES
# 
# 0 "DEFAULT_OPTIONS"
# 1 "DEFAULT_SEMANTIC"
# 2 "STATES_COLOR"
# 3 "STATES"
# 4 "EVENT_TYPE"
# 5 "GRADIENT_COLOR"
# 6 "GRADIENT_NAMES"
# 
def parsePCF():
	print ("Parsing " + PCF + ".....")

	f = open(PCF)

	state = -1
	line = f.readline()
	while line :
		if "\n" == line[0]:
			pass
		elif  "DEFAULT_OPTIONS" in line[0:15]:
			state = 0
		elif "DEFAULT_SEMANTIC" in line[0:16]:
			state = 1
		elif "STATES_COLOR" in line[0:12]:
			state = 2
		elif "STATES" in line[0:6]:
			state = 3
		elif "EVENT_TYPE" in line[0:10]:
			state = 4
		elif "GRADIENT_COLOR" in line[0:14]:
			state = 5
		elif "GRADIENT_NAMES" in line[0:14]:
			state = 6
		else:
			if state == -1:
				print ("Error parsing line " + line)
			elif state == 0:
				parsePCF_DEFAULT_OPTIONS(line)	
			elif state == 1:
				parsePCF_DEFAULT_SEMANTIC(line)
			elif state == 2:
				parsePCF_STATES_COLOR(line)
			elif state == 3:
				parsePCF_STATES(line)
			elif state == 4:
				parsePCF_EVENT_TYPE(line, f)
			elif state == 5:
				parsePCF_GRADIENT_COLOR(line)
			elif state == 6:
				parsePCF_GRADIENT_NAMES(line)
		line = f.readline()

	f.close()

#################################################################
#################################################################


#################################################################
###################### START POINT ##############################
#################################################################

# Checking arguments
if len(sys.argv) == 4 :
	for i in range(1,4) :
		if sys.argv[i].endswith(".prv") :
			PRV = sys.argv[i]
		if sys.argv[i].endswith(".pcf") :
			PCF = sys.argv[i]
		if sys.argv[i].endswith(".func") :
			FUNC = sys.argv[i]

	if PRV == "NOT FOUND" or PCF == "NOT FOUND"  or FUNC == "NOT FOUND":
		print ("Error, please provide .pcf .prv and .func")
		exit(1)
else:
	print ("Error, please provide .pcf .prv and func")
	exit(1)


# Parsing files
parseFUNC()
parsePCF()
parsePRV()

for t in threads:
	threads[t].createCharts()
