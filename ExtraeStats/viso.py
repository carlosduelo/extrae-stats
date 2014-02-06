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
		
			
		
