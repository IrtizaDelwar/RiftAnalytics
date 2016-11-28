class Champion:
	def __init__(self, champID):
		self.ID = champID
		self.spells = []
		
	def setChampName(self, champName):
		self.name = champName
		
	def setAbilities(self, spellList):
		for x in range(len(spellList)):
			self.spells.append(x)