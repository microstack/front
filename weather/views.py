from datetime import date, datetime
import calendar
import requests
import json

from flask import render_template
from flask import Flask

from utils.helper import get_weather_objects

app = Flask(__name__)


@app.route('/weather/')
def weather_mainpage():
    objects = get_weather_objects()

    return render_template('index.html', objects=objects)


@app.route('/weather/<string:date>/')
def specific_publish_weather(date):
    objects = get_weather_objects(date)

    return render_template('index.html', objects=objects)
