import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path='')

#apiKey = "RGAPI-fb1301bf-3c9e-4c02-8d6e-a00257350d0c"
apiKey = "a1c01d0f-b83b-4c38-89de-64de9b80ad5f"

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/profile/<region>/<username>')
def profile(region, username):
	userInfo = []
	masteryInfo = []
	usernameSearch = username.replace(" ", "")
	URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + usernameSearch + "?api_key=" + apiKey
	userInfo.append(username)
	searchResponse = requests.get(URL)
	if (valid_api_request(searchResponse) == False):
		errorReport = get_error(searchResponse)
		return render_template("invalid.html", error=errorReport)
	searchResponse = searchResponse.json()
	summonerIDs = searchResponse.get(usernameSearch.lower())
	iconID = str(summonerIDs.get('profileIconId'))
	URLICON = "http://ddragon.leagueoflegends.com/cdn/6.22.1/img/profileicon/"  + iconID + ".png"
	summonerID = summonerIDs.get('id')
	summonerLevel = summonerIDs.get('summonerLevel')
	userInfo.append(str(summonerLevel))
	if (summonerLevel != 30):
		userInfo.append("0")
		userInfo.append("0")
		userInfo.append("UNRANKED")
		userInfo.append("unranked")
		userInfo.append(URLICON)
		userInfo.append("No Games")
		userInfo.append("--")
	else:
		URLRANK  = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/by-summoner/" + str(summonerID) + "/entry?api_key=" + apiKey
		rankResponse = requests.get(URLRANK)
		rankResponse = rankResponse.json()
		rankData = rankResponse.get(str(summonerID))
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
	URLMASTERY = "https://na.api.pvp.net/championmastery/location/NA1/player/" + str(summonerID) + "/topchampions?count=5&api_key=" + apiKey
	masteryResponse = requests.get(URLMASTERY)
	masteryResponse = masteryResponse.json()
	URLSCORE = "https://na.api.pvp.net/championmastery/location/NA1/player/" + str(summonerID) + "/score?api_key=" + apiKey
	masteryScoreResponse = requests.get(URLSCORE)
	masteryScoreResponse = masteryScoreResponse.json()
	masteryInfo.append(str(masteryScoreResponse))
	for x in range(len(masteryResponse)):
		subInfo = []
		champID = str(masteryResponse[x].get('championId'))
		URLCHAMP = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + champID + "?champData=image&api_key=" + apiKey
		champResponse = requests.get(URLCHAMP)
		champResponse = champResponse.json()
		subInfo.append(str(champResponse.get('name')))
		picDict = champResponse.get('image')
		subInfo.append(picDict.get('full'))
		subInfo.append(str(masteryResponse[x].get('championLevel')))
		subInfo.append(str(masteryResponse[x].get('championPoints')))
		masteryInfo.append(subInfo)
	masteryInfo = valid_mastery(masteryInfo)
	return render_template("profile.html", name=username, stats=userInfo, mastery=masteryInfo)

@app.route('/ultimate-bravery')
def ultimate_bravery():
	return render_template("ultimate-bravery.html")

@app.route('/free-champion-rotation')
def free_champion_rotation():
	return render_template("free-champion-rotation.html")

@app.route('/champion_info', methods=['POST'])
def champion_info():
	#print('Hello world!', file=sys.stderr)
	champ_id = request.form['id']
	if champ_id:
		URL = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/champion/" + champ_id + "?champData=image&api_key=" + apiKey
		champInfoResponse = requests.get(URL)
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
	item_id = request.form['id']
	URL = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/item/" + item_id + "?itemData=image&api_key=" + apiKey
	itemInfoResponse = requests.get(URL)
	itemInfoResponse = itemInfoResponse.json()
	itemInfo = []
	itemInfo.append(str(itemInfoResponse.get('name')))
	picDict = itemInfoResponse.get('image')
	itemInfo.append(picDict.get('full'))
	return jsonify({'info' : itemInfo})

@app.route('/sspell_info', methods=['POST'])
def sspell_info():
	spell_id = request.form['id']
	spell_id2 = request.form['id2']
	URL = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/summoner-spell/" + spell_id + "?spellData=image&api_key=" + apiKey
	URL2 = "https://global.api.pvp.net/api/lol/static-data/na/v1.2/summoner-spell/" + spell_id2 + "?spellData=image&api_key=" + apiKey
	spellInfoResponse = requests.get(URL)
	spellInfoResponse2 = requests.get(URL2)
	spellInfoResponse = spellInfoResponse.json()
	spellInfoResponse2 = spellInfoResponse2.json()
	spellInfo = []
	spellInfo2 = []
	spellInfo.append(str(spellInfoResponse.get('name')))
	spellInfo2.append(str(spellInfoResponse2.get('name')))
	picDict = spellInfoResponse.get('image')
	picDict2 = spellInfoResponse2.get('image')
	spellInfo.append(picDict.get('full'))
	spellInfo2.append(picDict2.get('full'))
	return jsonify({'info' : spellInfo, 'info2' : spellInfo2})

@app.route('/champion_rotation', methods=['POST'])
def champion_rotation():
	URL = "https://na.api.pvp.net/api/lol/na/v1.2/champion?freeToPlay=true&api_key=" + apiKey
	freeChampionResponse = requests.get(URL)
	freeChampionResponse = freeChampionResponse.json()
	freeChampIDs = freeChampionResponse.get('champions')
	champIDs = []
	for x in range(len(freeChampIDs)):
		currentDict = freeChampIDs[x]
		currentChampID = str(currentDict.get('id'))
		champIDs.append(currentChampID)
	return jsonify({ 'info' : champIDs})

def valid_mastery(masteryInformationList):
	while (len(masteryInformationList) < 6):
		subInfo = []
		subInfo.append("Not Enough Champions")
		subInfo.append("Teemo.png")
		subInfo.append("0")
		subInfo.append("0")
		masteryInformationList.append(subInfo)
	return masteryInformationList;

def valid_api_request(apiResponse):
	if (apiResponse.status_code != 200):
		return False
	return True

def get_error(apiResponse):
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

if __name__ == "__main__":
	app.run(debug=True)