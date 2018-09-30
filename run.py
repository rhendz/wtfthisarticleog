## Runs the Flask API protocols
from flask import Flask, jsonify, request, render_template
import json
import os
app = Flask(__name__)

from main import getInitJSON

@app.route("/")
def init():
    return render_template('index.html')

@app.route("/<path:URL>")
def url_init(URL):
    getInitJSON(URL)
    with open('modules/json/bigJSON.json', 'r') as f:
        return jsonify(json.load(f))

if __name__ == '__main__':
    try:
        os.remove('modules/json/relatedLinks.json') # Special appended file
        os.remove('modules/json/bigJSON.json')
    except Exception as e:
        pass # This is fine, that means the links were already deleted
    app.run(debug=True)
