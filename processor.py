from flask import Flask, render_template

app = Flask(__name__, static_url_path='')

@app.route('/')
def index():
	return render_template("index.html")

@app.route('/profile/<username>')
def profile(username):
	return render_template("profile.html", name=username)

@app.route('/ultimate-bravery')
def ultimate_bravery():
	return render_template("ultimate-bravery.html")

if __name__ == "__main__":
	app.run(debug=True)