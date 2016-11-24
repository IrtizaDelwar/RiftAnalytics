from Processor import Processor
import requests

Processors = Processor()
results = Processors.searchUser("pvman", "kr")

print (results)
#free = Processors.freeChampions()
#print (free)