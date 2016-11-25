import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__, static_url_path='')

apiKey = "RGAPI-fb1301bf-3c9e-4c02-8d6e-a00257350d0c"

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/profile/<username>')
def profile(username):
	return render_template("profile.html", name=username)

@app.route('/ultimate-bravery')
def ultimate_bravery():
	return render_template("ultimate-bravery.html")

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

if __name__ == "__main__":
	app.run(debug=True)