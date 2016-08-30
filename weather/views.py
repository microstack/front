from datetime import date, datetime
import calendar
import requests
import json

from flask import render_template
from flask import Flask

from utils.helper import partial_by_index
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

    publish_weather = objects_from_request(API_GW_BASE_URL,
        '/weather/today/weather')

    '''
    weather cities are seperated by 7.
    for example,
    weather[0:7] is seoul weekdays weather
    '''
    num_weekdays = 7
    partial_publish_weather = partial_by_index(publish_weather, num_weekdays)

    today_publish = objects_from_request(API_GW_BASE_URL,
        '/weather/today/')

    first_date = datetime.strptime(publish_weather[0]['date'], '%Y-%m-%d')

    first_weekday = first_date.weekday()

    weekdays = calendar.day_abbr[first_weekday:] +\
        calendar.day_abbr[:first_weekday]

    objects['partial_weather'] = partial_publish_weather
    objects['publish'] = today_publish
    objects['first_weekday'] = weekdays[0]
    objects['weekdays'] = weekdays
    objects['main_weather'] = publish_weather[0]

    return render_template('index.html', objects=objects)
