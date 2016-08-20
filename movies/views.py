import requests
import os
import json

from flask import render_template
from flask import Flask

from settings import API_GW_BASE_URL

app = Flask(__name__)


def response_text_from_request(base_url, resource):
    response = requests.get(base_url + resource)
    text = response.text
    return text


@app.route('/movies/archive/')
def movie_archive():
    text = response_text_from_request(API_GW_BASE_URL, '/movies/')
    return text


@app.route('/movies/')
def movie_mainpage():
    text = response_text_from_request(API_GW_BASE_URL, '/movies/latest/')
    objects = json.loads(text)
    thumbnails = list(map(lambda x: x['thumbnail'], objects))
    return render_template('index.html', thumbnails=thumbnails)
