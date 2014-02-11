import application_data as ap
import numpy as np
import matplotlib.pyplot as plt 

class Viso:
	def __init__(self, _applicationData):
		self.appData = _applicationData
	
	def printAppTime(self):
		self.appData.printTime()

	def list_threads(self):
		self.appData.printListThreads()	
	
	def list_functions(self, thread = 0):
		self.appData.list_functions(thread)

	def list_intervals_function(self, thread, function):
		l = self.appData.getIntervalsFunction(thread, function)
		print ("Intervals of function " + str(function) + " on thread " + str(thread))
		for i in l:
			print (l[i])

	def nCalls_function(self, function):
		times = [0]
		threadL = [0]
		times += self.appData.nCalls_function(function)
		threadL += self.appData.getThreadsID()
		threadL.append(len(times))
		times.append(0)
		plt.bar(threadL, times)
		plt.xticks(np.arange(len(times))+0.4, threadL);
		plt.yticks(times)
		plt.xlabel("Threads")
		plt.ylabel("nCalls")
		plt.title("Function " + str(function) + " times called distribution")
		plt.show()

	def runningTime_function(self, function, thread):
		if thread == 0:
			minL = [0]
			maxL = [0]
			averageL = [0]
			threadL = [0]
			threadL += self.appData.getThreadsID()
			minL += self.appData.getMinCompleteTimeFunction(function)
			maxL += self.appData.getMaxCompleteTimeFunction(function)
			averageL += self.appData.getAverageCompleteTimeFunction(function)

			if	(len(minL) == 1 or
				len(maxL) == 1 or
				len(averageL) == 1 or
				len(threadL) == 1):
				print ("No data")
				return None

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
		else:
			minL = []
			maxL = []
			averageL = []
			intervals = []
			intervals += self.appData.getIntervalsFunction(thread, function)
			minL += self.appData.getMinIntervalsTimeFunction(thread, function)
			maxL += self.appData.getMaxIntervalsTimeFunction(thread, function)
			averageL += self.appData.getAverageIntervalsTimeFunction(thread, function)

			if	(len(minL) == 0 or
				len(maxL) == 0 or
				len(averageL) == 0 or
				len(intervals) == 0):
				print ("No data")
				return None

			width = 0.27
			t = np.array(intervals)
			plt.bar(t, minL, width=width, label='Min')
			plt.bar(t+width, averageL, width=width, color='red', label='Average')
			plt.bar(t+2*width, maxL, width=width, color='green', label='Max')
			plt.xticks(np.arange(len(minL))+0.4, intervals);
			plt.legend()
			plt.xlabel("Intervals")
			plt.ylabel("nanoseconds")
			plt.title("Function " + str(function) + " min, max and average running time")
			plt.show()

	def runningTime_thread(self, thread):
		minL = []
		maxL = []
		averageL = []
		functionsL = []
		functionsA = self.appData.getFunctions(thread)
		for e in functionsA:
			functionsL.append(e[0])
		minL += self.appData.getMinCompleteTimeThread(thread)
		maxL += self.appData.getMaxCompleteTimeThread(thread)
		averageL += self.appData.getAverageCompleteTimeThread(thread)

		print minL
		print maxL
		print averageL
		print functionsL

		if	(len(minL) == 0 or
			len(maxL) == 0 or
			len(averageL) == 0 or
			len(functionsL) == 0):
			print ("No data")
			return None

		width = 0.27
		t = np.array(functionsL)
		plt.bar(t, minL, width=width, label='Min')
		plt.bar(t+width, averageL, width=width, color='red', label='Average')
		plt.bar(t+2*width, maxL, width=width, color='green', label='Max')
		plt.xticks(t+0.4, functionsL);
		plt.legend()
		plt.xlabel("Functions")
		plt.ylabel("nanoseconds")
		plt.title("Thread " + str(thread) + " min, max and average running time of every function")
		plt.show()

	def threadsTimeline(self):
		fig, ax = plt.subplots()
		timelines = self.appData.getThreadsTimeLine()
		print timelines
		# Set y limits
		yw = 10
		ax.set_ylim(0,2*(len(timelines)+1)*yw )
		# Set x limits
		ax.set_xlim(0, timelines[1][1])
		yticks = []
		lyticks = []
		for i in timelines:
			ypos = 2*i*yw 
			yticks.append(ypos)
			lyticks.append(str(i))
			start = timelines[i][0]
			w = timelines[i][1] - timelines[i][0]
			ax.broken_barh([ (start, w), ] , (ypos - yw/2, yw))
		yticks.append(2*len(timelines)*yw)
		lyticks.append(str(len(timelines)))
		ax.set_xlabel('nanoseconds')
		ax.set_ylabel('threads')
		ax.set_yticks(yticks)
		ax.set_yticklabels(lyticks)
		plt.show()
