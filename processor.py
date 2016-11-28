import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path='')

#API Keys needed to access the data fromm the API. We have 2, because we are currently limited on how much data we can recieve.
apiKey2 = "RGAPI-fb1301bf-3c9e-4c02-8d6e-a00257350d0c"
apiKey = "a1c01d0f-b83b-4c38-89de-64de9b80ad5f"

@app.route('/')
def index():
	#Creates the HTML page the browser shows for the landing page of this website
	return render_template("index.html")

@app.route('/profile/<region>/<username>')
def profile(region, username):
	userInfo = []
	masteryInfo = []
	#Take out all spaces in the username, as the api does not include usernames
	usernameSearch = username.replace(" ", "")
	#Creates the URL for the API request to get the summoner ID of the summoner name passed in.
	URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + usernameSearch + "?api_key=" + apiKey
	userInfo.append(username)
	searchResponse = requests.get(URL)
	if (valid_api_request(searchResponse) == False):
		errorReport = get_error(searchResponse)
		return render_template("invalid.html", error=errorReport)
	searchResponse = searchResponse.json()
	summonerIDs = searchResponse.get(usernameSearch.lower())
	iconID = str(summonerIDs.get('profileIconId'))
	#Creates the URL for icon the username is using
	URLICON = "http://ddragon.leagueoflegends.com/cdn/6.22.1/img/profileicon/"  + iconID + ".png"
	summonerID = summonerIDs.get('id')
	summonerLevel = summonerIDs.get('summonerLevel')
	#If the username is not level 30, then initialize all the ranked stats to 0/unranked. As the API does not have any values for it.
	userInfo.append(str(summonerLevel))
	if (summonerLevel != 30):
		userInfo.append("0")
		userInfo.append("0")
		userInfo.append("UNRANKED")
		userInfo.append("unranked")
		userInfo.append(URLICON)
		userInfo.append("No Games")
		userInfo.append("--")
	else: #Else get the ranked stats for the username. Create the URL for the API request for the summoners ranked stats
		URLRANK  = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/by-summoner/" + str(summonerID) + "/entry?api_key=" + apiKey2
		rankResponse = requests.get(URLRANK)
		if (valid_api_request(rankResponse) == False):
			errorReport = get_error(rankResponse)
			return render_template("invalid.html", error=errorReport)
		rankResponse = rankResponse.json()
		rankData = rankResponse.get(str(summonerID))
		#Gets the data for solo ranked
		soloRankData = rankData[0]
		soloRankTier = soloRankData.get('tier')
		soloRankDivision = soloRankData.get('entries')
		soloRankDivision = soloRankDivision[0]
		soloRankDivisions = soloRankDivision.get('division')
		wins = soloRankDivision.get('wins')
		losses = soloRankDivision.get('losses')
		userInfo.append(str(wins))
		userInfo.append(str(losses))
		ratio = "{0:.2f}%".format(wins/(wins+losses) * 100)
		lp = soloRankDivision.get('leaguePoints')
		soloRankStats = str(soloRankTier) + " " + str(soloRankDivisions)
		userInfo.append(soloRankStats)
		soloRankImage = str(soloRankTier) + "Icon"
		userInfo.append(soloRankImage)
		userInfo.append(URLICON)
		userInfo.append(str(ratio))
		userInfo.append(str(lp))
	#Creates the URL for the mastery data for the user. We want the total mastery score, and top 5 champions based on mastery
	URLMASTERY = "https://" + region + ".api.pvp.net/championmastery/location/" + region + "1/player/" + str(summonerID) + "/topchampions?count=5&api_key=" + apiKey
	masteryResponse = requests.get(URLMASTERY)
	if (valid_api_request(masteryResponse) == False):
		errorReport = get_error(masteryResponse)
		return render_template("invalid.html", error=errorReport)
	masteryResponse = masteryResponse.json()
	URLSCORE = "https://" + region + ".api.pvp.net/championmastery/location/" + region + "1/player/" + str(summonerID) + "/score?api_key=" + apiKey2
	masteryScoreResponse = requests.get(URLSCORE)
	if (valid_api_request(masteryScoreResponse) == False):
		errorReport = get_error(masteryScoreResponse)
		return render_template("invalid.html", error=errorReport)
	masteryScoreResponse = masteryScoreResponse.json()
	masteryInfo.append(str(masteryScoreResponse))
	#Creates an array for each champion that is in the top mastery scores and adds the information the browser needs
	for x in range(len(masteryResponse)):
		subInfo = []
		champID = str(masteryResponse[x].get('championId'))
		URLCHAMP = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + champID + "?champData=image&api_key=" + apiKey
		champResponse = requests.get(URLCHAMP)
		if (valid_api_request(champResponse) == False):
			errorReport = get_error(champResponse)
			return render_template("invalid.html", error=errorReport)
		champResponse = champResponse.json()
		subInfo.append(str(champResponse.get('name')))
		picDict = champResponse.get('image')
		subInfo.append(picDict.get('full'))
		subInfo.append(str(masteryResponse[x].get('championLevel')))
		subInfo.append(str(masteryResponse[x].get('championPoints')))
		masteryInfo.append(subInfo)
	masteryInfo = valid_mastery(masteryInfo) #Make sure there is data for 5 masteries, as top 5 are displayed
	recentGame = recent_game(region, summonerID) #Get the information on the most recent game played by the user.
	return render_template("profile.html", name=username, stats=userInfo, mastery=masteryInfo, game=recentGame)

@app.route('/ultimate-bravery')
def ultimate_bravery():
	#Creates the HTML page that the browser shows when the user clicks on the "Ulimate Bravery" tab
	return render_template("ultimate-bravery.html")

@app.route('/free-champion-rotation')
def free_champion_rotation():
	#Creates the HTML page that the browser shows when the user clicks on the "Free champion Rotation" tab
	return render_template("free-champion-rotation.html")

@app.route('/champion_info', methods=['POST'])
def champion_info():
	#Creates the URL to make the api request for the champion needed
	champ_id = request.form['id']
	if champ_id:
		URL = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + champ_id + "?champData=image&api_key=" + apiKey
		champInfoResponse = requests.get(URL)
		if (valid_api_request(champInfoResponse) == False):
			errorReport = get_error(champInfoResponse)
			return render_template("invalid.html", error=errorReport)
		champInfoResponse = champInfoResponse.json()
		champInfo = []
		champInfo.append(str(champInfoResponse.get('name')))
		champInfo.append(str(champInfoResponse.get('title')))
		picDict = champInfoResponse.get('image')
		champInfo.append(picDict.get('full'))
		return jsonify({'info' : champInfo})
	return jsonify({'error' : 'API Request failed :('})

@app.route('/item_info', methods=['POST'])
def item_info():
	#Creates URL for the API request for the item needed
	item_id = request.form['id']
	URL = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/item/" + item_id + "?itemData=image&api_key=" + apiKey
	itemInfoResponse = requests.get(URL)
	if (valid_api_request(itemInfoResponse) == False):
		errorReport = get_error(itemInfoResponse)
		return render_template("invalid.html", error=errorReport)
	itemInfoResponse = itemInfoResponse.json()
	itemInfo = []
	#Gets the information needed from the dictionary and appends to the list it returns to the browser.
	itemInfo.append(str(itemInfoResponse.get('name')))
	picDict = itemInfoResponse.get('image')
	itemInfo.append(picDict.get('full'))
	return jsonify({'info' : itemInfo})

@app.route('/sspell_info', methods=['POST'])
def sspell_info():
	#Creates URLs for API request for the 2 summoner spells that we need information for.
	spell_id = request.form['id']
	spell_id2 = request.form['id2']
	URL = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/summoner-spell/" + spell_id + "?spellData=image&api_key=" + apiKey
	URL2 = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/summoner-spell/" + spell_id2 + "?spellData=image&api_key=" + apiKey
	spellInfoResponse = requests.get(URL)
	if (valid_api_request(spellInfoResponse) == False):
		errorReport = get_error(spellInfoResponse)
		return render_template("invalid.html", error=errorReport)
	spellInfoResponse2 = requests.get(URL2)
	if (valid_api_request(spellInfoResponse2) == False):
		errorReport = get_error(spellInfoResponse2)
		return render_template("invalid.html", error=errorReport)
	spellInfoResponse = spellInfoResponse.json()
	spellInfoResponse2 = spellInfoResponse2.json()
	spellInfo = []
	spellInfo2 = []
	#Gets the correct information needed to be displayed from the dictionaries and appends to list we give to the browser.
	spellInfo.append(str(spellInfoResponse.get('name')))
	spellInfo2.append(str(spellInfoResponse2.get('name')))
	picDict = spellInfoResponse.get('image')
	picDict2 = spellInfoResponse2.get('image')
	spellInfo.append(picDict.get('full'))
	spellInfo2.append(picDict2.get('full'))
	return jsonify({'info' : spellInfo, 'info2' : spellInfo2})

@app.route('/champion_rotation', methods=['POST'])
def champion_rotation():
	#Creates the URL for the API request to get the free chammpion rotation for the week.
	URL = "https://na.api.pvp.net/api/lol/na/v1.2/champion?freeToPlay=true&api_key=" + apiKey2
	freeChampionResponse = requests.get(URL)
	if (valid_api_request(freeChampionResponse) == False):
		errorReport = get_error(freeChampionResponse)
		return render_template("invalid.html", error=errorReport)
	freeChampionResponse = freeChampionResponse.json()
	freeChampIDs = freeChampionResponse.get('champions')
	champIDs = []
	#Since the API returns a dictionary of information. We want to parse through it to get the information the browser needs.
	for x in range(len(freeChampIDs)):
		currentDict = freeChampIDs[x]
		currentChampID = str(currentDict.get('id'))
		champIDs.append(currentChampID)
	return jsonify({ 'info' : champIDs})

def valid_mastery(masteryInformationList):
	#Makes sures that there is enough info in the mastery array, so that the browser can use it. If there isn't
	#that means the user did not have enough champions that have mastery scores. In that case set the values to 0.
	#The array must be size 5, because we display the top 5 champions based on mastery.
	while (len(masteryInformationList) < 6):
		subInfo = []
		subInfo.append("Not Enough Champions")
		subInfo.append("Teemo.png")
		subInfo.append("0")
		subInfo.append("0")
		masteryInformationList.append(subInfo)
	return masteryInformationList;

def valid_api_request(apiResponse):
	#Checks the http response. If the response = 200, that means the request was successful. Otherwise there was a error.
	if (apiResponse.status_code != 200):
		return False
	return True

def get_error(apiResponse):
	#Various Error codes that are sent by the API when the request fails.
	if (apiResponse.status_code == 404):
		return "Error 404: No summoner data found for the specified inputs. Please try a different summoner name or region."
	elif(apiResponse.status_code == 401):
		return "Error 401: The API Key is invalid, contact the administrator to fix the key."
	elif(apiResponse.status_code == 429):
		return "Error 429: The rate limit for the API Key was exceeded. Please wait a minute before trying again."
	elif(apiResponse.status_code == 500):
		return "Error 500: Internal service error. There is a problem with the Riot Games API."
	elif(apiResponse.status_code == 503):
		return "Error 503: The Riot Games API is currently unavailable."
	else:
		return "An unspecified error occured."

def recent_game(region, username):
	gameInfo = []
	#Creates URL for the API Requests, then requests it from the api
	URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.3/game/by-summoner/" + str(username) + "/recent?api_key=" + apiKey
	searchResponse = requests.get(URL)
	searchResponse = searchResponse.json()
	allGames = searchResponse.get('games')
	#Select the first game (most recent) in the array of games
	gameResponse = allGames[0]
	champion = gameResponse.get('championId')
	#URL to get the information for the champion the user played in their post recent game
	CHAMPURL = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + str(champion) + "?champData=image&api_key=" + apiKey
	champResponse = requests.get(CHAMPURL)
	champResponse = champResponse.json()
	#Get the dictionary of stats from the most recent game
	stats = gameResponse.get('stats')
	assists = stats.get('assists')
	gameInfo.append(str(champResponse.get('name')))
	picDict = champResponse.get('image')
	gameInfo.append(picDict.get('full'))
	assists = 0
	kills = stats.get('championsKilled')
	deaths = stats.get('numDeaths')
	assists = stats.get('assists')
	#Check that all values do get a response. If that entry doesn't exist in dictionary then set it 0
	if not stats.get('assists'):
		assists = 0
	if not stats.get('numDeaths'):
		deaths = 0
	if not stats.get('championsKilled'):
		kills = 0
	#Append a list of information to return to the browser
	gameInfo.append(str(kills))
	gameInfo.append(str(deaths))
	gameInfo.append(str(assists))
	gameInfo.append(str(stats.get('win')))
	print(str(stats.get('win')))
	KDA = "{0:.2f}".format((kills + assists) / deaths)
	gameInfo.append(str(KDA))
	return gameInfo

if __name__ == "__main__":
	app.run(debug=True)