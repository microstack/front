import requests
import json

from flask import render_template
from flask import Flask

from settings import API_GW_BASE_URL

app = Flask(__name__)


def response_text_from_request(base_url, resource):
    response = requests.get(base_url + resource)
    text = response.text
    return text


@app.route('/politics/bill/')
def politic_mainpage():
    bill_text = response_text_from_request(API_GW_BASE_URL, '/politics/bill/')
    items = json.loads(bill_text)
    bill_list = items['items']

    return render_template('index.html', bill_list=bill_list)
