#################################################################
######### Functions to parse FUNC file ##########################
#################################################################

class ParserFUNC:
	def __init__(self, _file_name):
		self.file_name = _file_name
		self.valid_functions = []

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
			try:
				self.valid_functions.append(int(line))
			except ValueError:
				print ("Error parsing line: " + line)
				exit(1)
			line = f.readline()

	def idFunctionValid(self, idF):
		return idF in self.valid_functions
	
	def printFunctions(self):
		print ("Functions: " + str(self.valid_functions))
	


#################################################################
#################################################################

