import requests
import User
import Item
import Champion
#import Player
#import Match

class Processor:
	#apiKey = "RGAPI-fb1301bf-3c9e-4c02-8d6e-a00257350d0c"
	def __init__(self):
		self.apiKey = "RGAPI-fb1301bf-3c9e-4c02-8d6e-a00257350d0c"

	def searchUser(self, username, region):
		URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + username + "?api_key=" + self.apiKey
		searchResponse = requests.get(URL)
		searchResponse = searchResponse.json()
		summonerIDs = searchResponse.get(username.lower())
		summonerID = summonerIDs.get('id')
		#return summonerIDs
		return str(summonerID)
		