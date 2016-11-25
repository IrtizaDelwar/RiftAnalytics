from Processor import Processor
import requests

Processors = Processor()
#Test to see if search user works
#results = Processors.searchUser("pvman", "kr")
#print (results)

#Test to see if free champions work
#free = Processors.freeChampions()
#print (free)

#Tests to see if getting champion info works
#champSearch = Processors.getChampionInfo("103")
#print (champSearch)

#Tests to see if getting item info works
itemSearch = Processors.getItemInfo(3085)
print (itemSearch)