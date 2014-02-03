#################################################################
######### Functions to parse PCF file ##########################
#################################################################

class Event:
	def __init__(self, _idE, _name):
		self.idE = _idE
		self.name = _name
		self.values = {}
	def __repr__(self):
		if len(self.values) == 0:
			return "Name \"" + self.name + "\" id " + str(self.idE)  + " values:  any"
		else:
			return "Name \"" + self.name + "\" id " + str(self.idE)  + " values: " + str(self.values)
	def __str__(self):
		if len(self.values) == 0:
			return "Name \"" + self.name + "\" id " + str(self.idE)  + " values:  any"
		else:
			return "Name \"" + self.name + "\" id " + str(self.idE)  + " values: " + str(self.values)

	def addValues(self, _values):
		self.values = _values

class ParserPCF:
	def __init__(self, _file_name):
		self.file_name= _file_name
		self.level = "THREAD"
		self.units = "NANOSECONDS"
		self.look_back = 100
		self.speed = 1
		self.num_state_colors = 1000
		self.ymax_scale	= 37
		self.states_color = {}
		self.states = {}
		self.gradient_name = {}
		self.gradient_color = {}
		self.events = {}
		self.__lastValues = {}
		self.__lastEvents = {}
		self.appEvent = 0
	
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
	def parseFile(self):
		print ("Parsing " + self.file_name + ".....")

		f = open(self.file_name)

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
				for i in self.__lastEvents:
					self.__lastEvents[i].addValues(self.__lastValues)
				self.__lastValues = {}
				self.__lastEvents = {}
				state = 4
			elif "GRADIENT_COLOR" in line[0:14]:
				state = 5
			elif "GRADIENT_NAMES" in line[0:14]:
				state = 6
			else:
				if state == -1:
					print ("Error parsing line " + line)
				elif state == 0:
					self.__parsePCF_DEFAULT_OPTIONS(line)	
				elif state == 1:
					self.__parsePCF_DEFAULT_SEMANTIC(line)
				elif state == 2:
					self.__parsePCF_STATES_COLOR(line)
				elif state == 3:
					self.__parsePCF_STATES(line)
				elif state == 4:
					self.__parsePCF_EVENT_TYPE(line, f)
				elif state == 5:
					self.__parsePCF_GRADIENT_COLOR(line)
				elif state == 6:
					self.__parsePCF_GRADIENT_NAMES(line)
			line = f.readline()

		for i in self.__lastEvents:
			self.__lastEvents[i].addValues(self.__lastValues)
		self.__lastValues = {}
		self.__lastEvents = {}
		f.close()

	def __parsePCF_DEFAULT_OPTIONS(self, line):
		if "LEVEL" in line[0:5]:
			elements = line.split()
			self.level = elements[1]
		elif "UNITS" in line[0:5]:
			elements = line.split()
			self.units = elements[1]
		elif "LOOK_BACK" in line[0:9]:
			elements = line.split()
			try:
				self.look_back = int(elements[1])
			except ValueError:
				print ("Error parsing line: " + line)
		elif "SPEED" in line[0:5]:
			elements = line.split()
			try:
				self.speed = int(elements[1])
			except ValueError:
				print ("Error parsing line: " + line)
		elif "FLAG_ICONS" in line[0:10]:
			pass
		elif "NUM_OF_STATE_COLORS" in line[0:19]:
			elements = line.split()
			try:
				self.num_state_colors = int(elements[1])
			except ValueError:
				print ("Error parsing line: " + line)
		elif "YMAX_SCALE" in line[0:10]:
			elements = line.split()
			try:
				self.ymax_scale = int(elements[1])
			except ValueError:
				print ("Error parsing line: " + line)
		elif "\n" in line[0]:
			pass
		else:
			print ("Error parsing line: " + line)

	def __parsePCF_DEFAULT_SEMANTIC(self, line):
		if "THREAD_FUNC" in line[0:11]:
			pass
		elif "\n" in line[0]:
			pass
		else:
			print ("Error parsing line: " + line)

	def __parsePCF_STATES_COLOR(self, line):
		if "\n" in line[0]:
			pass
		else:
			elements = line.split()
			try:
				i = int(elements[0])
				c = elements[1][1:-1].split(",")
				self.states_color[i] = (int(c[0]),int(c[1]),int(c[2]))
			except ValueError:
				print ("Error parsing line: " + line)

	def __parsePCF_STATES(self, line):
		if "\n" in line[0]:
			pass
		else:
			elements = line.split()
			try:
				s = int(elements[0])
				self.states[s] = elements[1] 
			except ValueError:
				print ("Error parsing line " + line)
		
	def __parsePCF_EVENT_TYPE(self, line, f):
		if "\n" in line[0]:
			pass
		elif "VALUES" in line[0:6]:
			l = f.readline()
			while l != "\n":
				elements = l.split()
				try:
					v = int(elements[0])
					self.__lastValues[v] = " ".join(elements[1:])
				except ValueError:
					print ("Error parsing line " + line)
				l = f.readline()
		else:
			elements = line.split()
			try:
				e = int(elements[1])
				n = " ".join(elements[2:])
				self.events[e] = Event(e, n)
				self.__lastEvents[e] = self.events[e]

				if self.events[e].name == "Application":
					self.appEvent = e	
			except ValueError:
				print ("Error parsing line " + line)

	def __parsePCF_GRADIENT_COLOR(self, line):
		if "\n" in line[0]:
			pass
		else:
			elements = line.split()
			try:
				i = int(elements[0])
				c = elements[1][1:-1].split(",")
				self.gradient_color[i] = (int(c[0]),int(c[1]),int(c[2]))
			except ValueError:
				print ("Error parsing line " + line)

	def __parsePCF_GRADIENT_NAMES(self, line):
		if "\n" in line[0]:
			pass
		else:
			elements = line.split()
			try:
				s = int(elements[0])
				self.gradient_name[s] = " ".join(elements[1:])
			except ValueError:
				print ("Error parsing line " + line)

	def isAppEvent(self, e):
		return self.appEvent == e

	def printDefaultOptions(self):
		print ("File name: " + self.file_name)
		print ("Level: " + self.level)
		print ("Units: " + self.units)
		print ("Look_back: " + str(self.look_back))
		print ("Speed: " + str(self.speed))
		print ("Num state colors: " + str(self.num_state_colors))
		print ("ymax_scale: " + str(self.ymax_scale))

	def printStates(self):
		for i in self.states:
			print ("State \"" + str(self.states[i]) + "\" id " + str(i) + " color " + str(self.states_color[i]))

	def printGradients(self):
		for i in self.gradient_name:
			print ("Gradient \"" + str(self.gradient_name[i]) + "\" id " + str(i) + " color " + str(self.gradient_color[i]))

	def printEvents(self):
		for i in self.events:
			print (self.events[i])

#################################################################
#################################################################
