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
		userInfo = []
		URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + username + "?api_key=" + self.apiKey
		userInfo.append(username)
		searchResponse = requests.get(URL)
		searchResponse = searchResponse.json()
		summonerIDs = searchResponse.get(username.lower())
		summonerID = summonerIDs.get('id')
		summonerLevel = summonerIDs.get('summonerLevel')
		userInfo.append(str(summonerLevel))
		URLRANK  = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/by-summoner/" + str(summonerID) + "/entry?api_key=" + self.apiKey
		rankResponse = requests.get(URLRANK)
		rankResponse = rankResponse.json()
		rankData = rankResponse.get(str(summonerID))
		soloRankData = rankData[0]
		soloRankTier = soloRankData.get('tier')
		soloRankDivision = soloRankData.get('entries')
		soloRankDivision = soloRankDivision[0]
		soloRankDivision = soloRankDivision.get('division')
		soloRankStats = str(soloRankTier) + " " + str(soloRankDivision)
		userInfo.append(soloRankStats)
		#return summonerIDs
		return userInfo
		
	def freeChampions(self):
		URL = "https://na.api.pvp.net/api/lol/na/v1.2/champion?freeToPlay=true&api_key=" + self.apiKey
		freeChampionResponse = requests.get(URL)
		freeChampionResponse = freeChampionResponse.json()
		freeChampIDs = freeChampionResponse.get('champions')
		champIDs = []
		for x in range(len(freeChampIDs)):
			currentDict = freeChampIDs[x]
			currentChampID = str(currentDict.get('id'))
			ChampURL = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + currentChampID + "?api_key=" + self.apiKey
			champInfo = requests.get(ChampURL)
			champInfo = champInfo.json()
			champName = str(champInfo.get('name'))
			champIDs.append(champName)
		return champIDs
		
	def getChampionInfo(self, champID):
		URL = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + champID + "?champData=image&api_key=" + self.apiKey
		champInfoResponse = requests.get(URL)
		champInfoResponse = champInfoResponse.json()
		champInfo = []
		champInfo.append(str(champInfoResponse.get('name')))
		champInfo.append(str(champInfoResponse.get('title')))
		picDict = champInfoResponse.get('image')
		champInfo.append(picDict.get('full'))
		return champInfo
		
	def getItemInfo(self, itemID):
		URL = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/item/" + str(itemID) + "?itemData=image&api_key=" + self.apiKey
		itemInfoResponse = requests.get(URL)
		itemInfoResponse = itemInfoResponse.json()
		itemInfo = []
		itemInfo.append(str(itemInfoResponse.get('name')))
		picDict = itemInfoResponse.get('image')
		itemInfo.append(picDict.get('full'))
		return itemInfo
		