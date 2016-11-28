class User:
	#The class contains information for a user include name, their ID, level, and solo Rank
	def __init__(self, name):
		self.username = name
		
	#Sets the User's ID as a string.
	def setNameID(self, nameID):
		self.ID = nameID
	
	#Sets the user's level as a string
	def setLevel(self, curLevel):
		self.level = curLevel
		
	#Sets the user's current solo rank as a string.
	def setSoloRank(self, curRank):
		self.soloRank = curRank