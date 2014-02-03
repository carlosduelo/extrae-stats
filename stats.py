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
	parserPRV.printAppTime()

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

parserPRV = pPRV.ParserPRV(PRV, parserPFC, parserFUNC)
parserPRV.parseFile()
# parserPRV.printAppTime()

#for t in threads:
#	threads[t].createCharts()

# Start ipython for interactive charts
from IPython import embed
embed()
