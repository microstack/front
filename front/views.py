import os

from flask import render_template
from flask import Flask
app = Flask(__name__)

import requests

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies/')
def movie_mainpage():
    url = os.environ.get('API_GW_URL')
    port = os.environ.get('API_GW_PORT')
    response = requests.get(url + ':' + port + '/movies/')
    text = response.text

    return text

@app.route('/actors/')
def actor_mainpage():
    return 'Actor mainpage'

@app.route('/other-page/')
def other_page():
    return 'Here from /other-page/'
