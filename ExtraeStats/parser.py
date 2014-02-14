import parseFUNC as pFUNC
import parsePCF as pPCF
import parsePRV as pPRV

class Parser:
	def __init__(self, _file_name_FUNC,  _file_name_PCF, _file_name_PRV):
		self.file_name_FUNC = _file_name_FUNC
		self.file_name_PCF  = _file_name_PCF
		self.file_name_PRV = _file_name_PRV
		self.parserFUNC = pFUNC.ParserFUNC(self.file_name_FUNC)
		self.parserPFC = pPCF.ParserPCF(self.file_name_PCF)
		self.parserPRV = pPRV.ParserPRV(self.file_name_PRV, self.parserPFC, self.parserFUNC)

	def parseFiles(self):
		self.parserFUNC.parseFile()
		self.parserPFC.parseFile()
		self.parserPRV.parseFile()

	def getApplicationData(self):
		return self.parserPRV.getApplicationData()
	
	def getNameEvent(self, e):
		return self.parserPFC.getNameEvent(e)
	
	def getLineMarks(self, function):
		return self.parserFUNC.getLineMarks(function)
