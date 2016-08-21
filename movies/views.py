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
    latest_text = response_text_from_request(API_GW_BASE_URL, '/movies/latest/')
    grade_text = response_text_from_request(API_GW_BASE_URL, '/movies/grade/')


    latest_objects = json.loads(latest_text)
    grade_objects = json.loads(grade_text)

    latest_thumbnails = list(map(lambda x: x['thumbnail'], latest_objects))
    return render_template('index.html', latest_thumbnails=latest_thumbnails,
        high_grades=grade_objects)
