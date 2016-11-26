import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path='')

apiKey = "RGAPI-fb1301bf-3c9e-4c02-8d6e-a00257350d0c"

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/profile/<region>/<username>')
def profile(region, username):
	userInfo = []
	URL = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v1.4/summoner/by-name/" + username + "?api_key=" + apiKey
	userInfo.append(username)
	searchResponse = requests.get(URL)
	searchResponse = searchResponse.json()
	summonerIDs = searchResponse.get(username.lower())
	summonerID = summonerIDs.get('id')
	summonerLevel = summonerIDs.get('summonerLevel')
	userInfo.append(str(summonerLevel))
	#self.userID = str(summonerID)
	URLRANK  = "https://" + region + ".api.pvp.net/api/lol/" + region + "/v2.5/league/by-summoner/" + str(summonerID) + "/entry?api_key=" + apiKey
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
	return render_template("profile.html", name=username, stats=userInfo)

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

if __name__ == "__main__":
	app.run(debug=True)