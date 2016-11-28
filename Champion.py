class Champion:
	#This class contains information about a champion including it's name, id, and it's spells
	#Constructor that initializes the champion's spell array and sets it's champion ID.
	def __init__(self, champID):
		self.ID = champID
		self.spells = []
		
	#Sets the name of the champion.
	def setChampName(self, champName):
		self.name = champName
		
	#Takes in a list of spells and appends it to the champion's list of spells.
	def setAbilities(self, spellList):
		for x in range(len(spellList)):
			self.spells.append(x)