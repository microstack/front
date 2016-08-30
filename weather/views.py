import requests
import json

from flask import render_template
from flask import Flask

from settings import API_GW_BASE_URL

app = Flask(__name__)


def response_text_from_request(base_url, resource):
    try:
        response = requests.get(base_url+resource)
    except requests.ConnectionError:
        text = "{'error': 'ConnectionError'}"
        return text

    if response.status_code != 200:
        text = "{'error': 'Statuscode : %s' % response.status_code}"
        return text

    text = response.text
    return text


def objects_from_request(base_url, resource):
    text = response_text_from_request(base_url, resource)
    objects = json.loads(text)
    return objects


def is_error_in_objects(objects):
    for key in objects.keys():
        if isinstance(objects[key], (list, str)):
            continue

        if objects[key].get('error'):
            return True
    return False


@app.route('/weather/')
def weather_mainpage():
    objects = dict()

    today_weather = objects_from_request(API_GW_BASE_URL,
        '/weather/today/weather')
    today_publish = objects_from_request(API_GW_BASE_URL,
        '/weather/today/')

    objects['weather'] = today_weather
    objects['publish'] = today_publish
    
    return render_template('index.html', objects=objects)
