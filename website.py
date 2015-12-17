import json
import flask
from flask import Flask, request, render_template
app = Flask(__name__)

# home page
@app.route('/')
def index():

	with open('super-bowl-play-by-play.json') as f:
		data = json.load(f)

	rushers = {}
	for j in xrange(len(data['periods'])):

		for i in data['periods'][j]['pbp']:
			if i['type'] == 'drive':

				for event in i['events']:
					if 'statistics' in event.keys() and event['play_type'] == 'rush':
						rusher = event['statistics'][0]['player']['name']
						if rusher not in rushers.keys():
							rushers[rusher] = event['statistics'][0]['yards']
						else:
							rushers[rusher] = event['statistics'][0]['yards'] + rushers[rusher]

	rushers_sorted = [(rusher, rushers[rusher]) for rusher in sorted(rushers, key=rushers.get, reverse= True)]
	return render_template('table.html', rushers=rushers_sorted)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=8000, debug=True)