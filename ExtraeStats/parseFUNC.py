#################################################################
######### Functions to parse FUNC file ##########################
#################################################################

class ParserFUNC:
	def __init__(self, _file_name):
		self.file_name = _file_name
		self.valid_functions = []
		self.lineMarks = {}

	def parseFile(self):
		print ("Parsing " + self.file_name + ".....")

		f = open(self.file_name)
		line = f.readline()

		if "#Functions" in line[0:10]:
			line = f.readline()
		else:
			print ("Error no Functions file")
			exit(1)

		while line :
			elements = line.split()
			try:
				idF = int(elements[0])
				self.valid_functions.append(idF)
				self.lineMarks[idF] = {}
				for i in range(1,len(elements),2):
					l = int(elements[i])
					v = int(elements[i+1])
					self.lineMarks[idF][v] = l
			except ValueError:
				print ("ValueException catched: Error parsing line: " + line)
				exit(1)
			except IndexError:
				print ("IndexError catched: Error parsing line: " + line)
				exit(1)
			line = f.readline()

	def idFunctionValid(self, idF):
		return idF in self.valid_functions
	
	def printFunctions(self):
		print ("Functions: " + str(self.valid_functions))

	def getLineMarks(self, function):
		if function in self.lineMarks:
			return self.lineMarks[function]
		else:
			return {}
	


#################################################################
#################################################################

