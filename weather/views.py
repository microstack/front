from datetime import date, datetime
import calendar
import requests
import json

from flask import render_template
from flask import Flask

from utils.helper import get_weather_objects,\
    get_template_name_from_objects_status

app = Flask(__name__)


@app.route('/')
def weather_mainpage():
    objects = get_weather_objects()
    template_name = get_template_name_from_objects_status(objects,
        'index.html')

    return render_template(template_name, objects=objects)


@app.route('/<string:date>/')
def specific_publish_weather(date):
    objects = get_weather_objects(date)
    template_name = get_template_name_from_objects_status(objects,
        'index.html')

    return render_template(template_name, objects=objects)
