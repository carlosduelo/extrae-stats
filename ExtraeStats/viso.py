import parser as pr 
import application_data as ap
import numpy as np
import matplotlib.pyplot as plt 
import networkx as nx
import math

class Viso:
	def __init__(self, _parser):
		self.parser = _parser
		self.appData = _parser.getApplicationData()
	
	def printAppTime(self):
		self.appData.printTime()

	def list_threads(self):
		self.appData.printListThreads()	
	
	def list_functions(self, thread = 0):
		self.appData.list_functions(thread)

	def list_intervals_function(self, thread, function):
		lineMarks = self.parser.getLineMarks(function)
		print ("Intervals of function " + str(function) + " on thread " + str(thread))
		for i in range(1, len(lineMarks)):
			print ("Interval " + str(i-1) + " lines: " + str(lineMarks[i]) + " - " + str(lineMarks[i+1]))
		print ("Interval " + str(len(lineMarks)-1) + " lines: " + str(lineMarks[len(lineMarks)]) + " -  end function")


	def nCalls_function(self, function, thread):
		if thread == 0:
			times = [0]
			threadL = [0]
			times += self.appData.nCalls_function(function, thread)
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
		else:
			times = []
			threadL = []
			times += self.appData.nCalls_function(function, thread)
			threadL += self.appData.getIntervalsFunction(thread, function)
			plt.bar(threadL, times)
			plt.xticks(np.arange(len(times))+0.4, threadL);
			plt.yticks(times)
			plt.xlabel("Intervals")
			plt.ylabel("nCalls")
			plt.title("Function " + str(function) + " times called in different intervals")
			plt.show()

	def nCalls_thread(self, thread):
		functionT = self.appData.getFunctions(thread)
		times = []
		functionL = []
		if thread == 0:
			for i in range(0, len(functionT)):
				f = functionT[i][0]
				times.append(sum(self.appData.nCalls_function(f,0)))
				functionL.append(f)
		else:
			for i in range(0, len(functionT)):
				f = functionT[i][0]
				times.append(self.appData.nCalls_function_in_thread(f, thread))
				functionL.append(f)

		print functionL
		print times
		t = np.array(functionL)
		plt.bar(t, times)
		plt.xticks(t+0.4, functionL);
		plt.bar(functionL, times)
		plt.xlabel("Functions")
		plt.ylabel("nCalls")
		plt.title("Function times called distribution")
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

	def runningAvgTime_function(self, function, thread):
		if thread == 0:
			averageL = [0]
			threadL = [0]
			threadL += self.appData.getThreadsID()
			averageL += self.appData.getAverageCompleteTimeFunction(function)

			if	(len(averageL) == 1 or
				len(threadL) == 1):
				print ("No data")
				return None

			threadL.append(len(threadL))
			averageL.append(0)
			t = np.array(threadL)
			plt.bar(t, averageL)
			plt.xticks(t+0.4, threadL);
			plt.legend()
			plt.xlabel("Threads")
			plt.ylabel("nanoseconds")
			plt.title("Function " + str(function) + " average running time")
			plt.show()
		else:
			averageL = []
			intervals = []
			intervals += self.appData.getIntervalsFunction(thread, function)
			averageL += self.appData.getAverageIntervalsTimeFunction(thread, function)

			if	(len(averageL) == 0 or
				len(intervals) == 0):
				print ("No data")
				return None

			t = np.array(intervals)
			plt.bar(t, averageL)
			plt.xticks(t+0.4, intervals);
			plt.legend()
			plt.xlabel("Intervals")
			plt.ylabel("nanoseconds")
			plt.title("Function " + str(function) + " average running time")
			plt.show()

	def listRunningAvgTime_function(self, function, thread):
		averageL = []
		intervals = []
		intervals += self.appData.getIntervalsFunction(thread, function)
		averageL += self.appData.getAverageIntervalsTimeFunction(thread, function)

		print ("Function " + str(function) + " average running time")
		for i in range(0,len(intervals)):
			print("\tInterval " + str(intervals[i]) + " " + str(averageL[i]) + " nanoseconds")
	
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
		# add application time
		timelines[0] = (self.appData.timeStart, self.appData.timeEnd)
		print "-----"
		print timelines
		# Set y limits
		yw = 10
		ax.set_ylim(-10 ,2*(max(timelines.keys())+1)*yw )
		# Set x limits
		ax.set_xlim(0, timelines[0][1])
		yticks = []
		lyticks = []
		for i in timelines:
			ypos = 2*i*yw 
			yticks.append(ypos)
			start = timelines[i][0]
			w = timelines[i][1] - timelines[i][0]
			if i == 0:
				lyticks.append("Application")
				ax.broken_barh([ (start, w), ] , (ypos - yw/2, yw))
			else:
				lyticks.append("Thread "+str(i))
				ax.broken_barh([ (start, w), ] , (ypos - yw/2, yw))
		ax.set_xlabel('nanoseconds')
		ax.set_ylabel('threads')
		ax.set_yticks(yticks)
		ax.set_yticklabels(lyticks)
		ax.legend() 
		plt.show()

	def runningAvgTime_thread(self, thread):
		averageL = []
		functionsL = []
		functionsA = self.appData.getFunctions(thread)
		for e in functionsA:
			functionsL.append(e[0])
		averageL += self.appData.getAverageCompleteTimeThread(thread)

		if	(len(averageL) == 0 or
			len(functionsL) == 0):
			print ("No data")
			return None

		t = np.array(functionsL)
		plt.bar(t, averageL)
		plt.xticks(t+0.4, functionsL);
		plt.legend()
		plt.xlabel("Functions")
		plt.ylabel("nanoseconds")
		plt.title("Thread " + str(thread) + " average running time of every function")
		plt.show()

	def listRunningAvgTime_thread(self, thread):
		averageL = []
		functionsL = []
		functionsA = self.appData.getFunctions(thread)
		for e in functionsA:
			functionsL.append(e[0])
		averageL += self.appData.getAverageCompleteTimeThread(thread)
		print ("Thread " + str(thread) + " average running time of every function")
		for i in range(0,len(functionsL)):
			print ("\t Function " + str(functionsL[i]) + " average time " + str(averageL[i]) + " nanoseconds")

	def thread_function_summary(self, thread):
		appTime = self.appData.getCompleteTimeThread(thread)
		other = appTime
		averageL = []
		functionsL = []
		functionsA = self.appData.getFunctions(thread)
		labels = []
		percen = []
		for e in functionsA:
			functionsL.append(e[0])
			labels.append(str(e[0]))
		averageL += self.appData.getCompleteTimeFunctionsThread(thread)
		for i in range(0,len(averageL)):
			other -= averageL[i] 
			p = (averageL[i]*100.0)/float(appTime)
			labels[i] += " %.2g " % p + " %"
			percen.append(p)

		if other < 0:
			print ("Error function time recollected is greater than application time")
		# Others
		labels.append("Others")
		percen.append((other*100.0)/float(appTime))

		if	(len(averageL) == 0 or
			len(functionsL) == 0):
			print ("No data")
			return None

		patches, texts = plt.pie(percen)
		plt.legend(patches, labels, loc="best")
		plt.show()

	def drawThreadTree(self, thread):
		tree = self.appData.getThreadTree(thread)
		if len(tree) == 0:
			print ("Enter a correct thread id")
			return
		G = nx.MultiDiGraph()
		print tree
		for f in tree:
			G.add_node(f)
			if len(tree[f]) > 0:
				for ff in tree[f]:
					G.add_edge(f, ff)
		nx.draw(G)
		plt.show()
