class Item:
	#This class contains information about items such as id, name, and description.
	#Construct that initializes the item object and stores it's ID
	def __init__(self, itemID):
		self.ID = itemID
	
	#This method sets the name of the item object.
	def setName(self, itemName):
		self.name = itemName
	
	#This method sets the description of the item object.
	def setDescription(self, itemDes):
		self.description = itemDes