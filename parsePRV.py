#################################################################
######### Functions to parse PRV file ##########################
#################################################################

import application as ap

class ParserPRV:
	def __init__(self, _file_name, _parserPCF, _parserFUNC):
		self.file_name = _file_name
		self.parserPCF = _parserPCF
		self.parserFUNC = _parserFUNC
		self.app		= ap.Application()

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

					timeStamp = int(elements[5])
					for i in range(6,len(elements), 2):
						e = int(elements[i])
						if self.parserPCF.isAppEvent(e):
							v = int(elements[i+1])
							if v:
								self.app.addStart(timeStamp)
							else:
								self.app.addEnd(timeStamp)

						elif self.parserFUNC.idFunctionValid(e):
							v = int(elements[i+1])
							#print ("Thread " + str(thread) + " timeStamp " + str(timeStamp) + " event " + str(e) + " value " + str(v))
							self.app.addEventFunction(thread, timeStamp, e, v)
						elif self.parserPCF.isEvent(e):
							self.app.addEvent(thread, timeStamp, e, v)
						else:
							print("Undifined event " + str(e))



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

	def	printAppTime(self):
		self.app.printTime()

#################################################################
#################################################################

