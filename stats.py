#!/usr/bin/env python

import sys
import pylab
import numpy as np
import matplotlib.pyplot as plt 
import parseFUNC as pFUNC
import parsePCF as pPCF
import parsePRV as pPRV

print ("Creating statistics....")

# File names
PRV="NOT FOUND"
PCF="NOT FOUND"
FUNC="NOT FOUND"

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
        
# Global variables
states = {}
events = {} 
valid_events = []
threads ={}


#################################################################
#################### SHELL FUNCTIONS ############################
#################################################################

def help_commands():
	print ("Commands: ")
	print ("application_time()	- show elapsed real time used by the application in nanoseconds")
	print ("list_threads()	- show threads executed")
	print ("list_functions( [thread] )	- list all functions, if a thread id is provided list all the functions called in the thread")
	print ("threads_timeline()	- show thread timeline")
	print ("nCalls_function( <function> )	- number of times a function is called")
	print ("runningTime_function(<function>, [thread] ) - min, max and average running time of a function")

def application_time():
	print("Application time: " + str(application.getCompleteTime()) + " nanoseconds")

def list_threads():
	for t in threads:
		threads[t].printDetail()

def list_functions( thread = 0 ):
	if thread == 0:
		for i in valid_events:
			print(events[i])	
	else:
		if thread in threads:
			threads[thread].printListFunctions()
		else:
			print ("Please, enter a correct thread id")
	
def nCalls_function(function):
	times = [0]
	threadL = [0]
	for t in threads:
		times.append(threads[t].nCallsFunction(function))
		threadL.append(t)
	threadL.append(len(times))
	times.append(0)
	plt.bar(threadL, times)
	plt.xticks(np.arange(len(times))+0.4, threadL);
	plt.yticks(times)
	plt.xlabel("Threads")
	plt.ylabel("nCalls")
	plt.title("Function " + str(function) + " times called distribution")
	plt.show()

def runningTime_function(function, thread=0):
	if thread == 0:
		minL = [0]
		maxL = [0]
		averageL = [0]
		threadL = [0]
		for t in threads:
			minL.append(100)
			maxL.append(4000)
			averageL.append(2000)
			threadL.append(t)

		threadL.append(len(threadL))
		minL.append(0)
		maxL.append(0)
		averageL.append(0)
		width = 0.27
		t = np.array(threadL)
		plt.bar(t, minL, width=width, label='Min')
		plt.bar(t+width, averageL, width=width, color='red', label='Average')
		plt.bar(t+2*width, maxL, width=width, color='green', label='Max')
		plt.xticks(np.arange(len(minL))+0.4, threadL);
		plt.legend()
		plt.xlabel("Threads")
		plt.ylabel("nanoseconds")
		plt.title("Function " + str(function) + " min, max and average running time")
		plt.show()
	elif thread in threads:
		print ("OK")
	else:
		print ("Please provide a correct thread id")
		
			

def threads_timeline():
	plt.figure()
	x = pylab.randn(10000)
	plt.hist(x, 100)
	plt.show()
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
parserFUNC = pFUNC.ParserFUNC(FUNC)
parserFUNC.parseFile()
# parserFUNC.printFunctions()

parserPFC = pPCF.ParserPCF(PCF)
parserPFC.parseFile()
# parserPFC.printDefaultOptions()
# parserPFC.printStates()
# parserPFC.printGradients()
# parserPFC.printEvents()

parserPRV = pPRV.ParserPRV(PRV, parserPFC)
parserPRV.parseFile()
# parserPRV.printAppTimes()

#for t in threads:
#	threads[t].createCharts()

# Start ipython for interactive charts
#from IPython import embed
#embed()
