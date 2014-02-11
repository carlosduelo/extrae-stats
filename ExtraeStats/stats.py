#!/usr/bin/env python

import sys
import parser as pr
import viso

print ("Creating statistics....")

# Global variables
PRV="NOT FOUND"
PCF="NOT FOUND"
FUNC="NOT FOUND"

#################################################################
#################### SHELL FUNCTIONS ############################
#################################################################

def help_commands():
	print ("Commands: ")
	print ("application_time()	- show elapsed real time used by the application in nanoseconds")
	print ("list_threads()	- show threads executed")
	print ("list_functions( [thread] )	- list all functions, if a thread id is provided list all the functions called in the thread")
	print ("list_intervals_function( thread, function) - list all intervals inside of a function")
	print ("threads_timeline()	- show thread timeline")
	print ("nCalls_function( <function>, [thread]  )	- number of times a function is called")
	print ("runningTime_function(<function>, [thread] ) - min, max and average running time of a function")
	print ("runningTime_thread( <thread> ) - min, max, and average running time of every function on a thread")
	print ("seeSorceCode( <function> )")

def application_time():
	vis.printAppTime()

def list_threads():
	vis.list_threads()

def list_functions( thread = 0 ):
	vis.list_functions(thread)

def list_intervals_function(thread, function):
	vis.list_intervals_function(thread, function)
	
def nCalls_function(function, thread=0):
	vis.nCalls_function(function, thread)

def runningTime_function(function, thread=0):
	vis.runningTime_function(function, thread)

def runningTime_thread(thread):
	vis.runningTime_thread(thread)

def threads_timeline():
	vis.threadsTimeline()
	
def seeSourceCode(function):
	n = parser.getNameEvent(function)
	if n != "":
		elements = n.split(":")
		nombre = elements[0] 
		mgc = get_ipython().magic
		mgc("%edit " + nombre)
	else:
		print ("Event does not exist")
#################################################################
#################################################################

#################################################################
###################### START POINT ##############################
#################################################################

# Checking arguments
if len(sys.argv) == 4:
	for i in range(1,4):
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
parser = pr.Parser(FUNC, PCF, PRV)
parser.parseFiles()

# Create Viso object
vis = viso.Viso(parser.getApplicationData())

# Start ipython for interactive charts
from IPython import embed
embed()
