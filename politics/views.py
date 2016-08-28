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
def bill_list():
    resource = '/politics/bill/'
    bill_text = response_text_from_request(API_GW_BASE_URL, resource)
    items = json.loads(bill_text)
    bill_list = items['items']

    return render_template('index.html', bill_list=bill_list)


@app.route('/politics/bill/<int:id>/')
def bill_detail(id):
    resource = '/politics/bill/%s' % id
    bill_text = response_text_from_request(API_GW_BASE_URL, resource)
    bill = json.loads(bill_text)

    summary_list = []
    if bill['summary'] is None:
        text = '해당 의안에 대한 정보는 준비중입니다.'
        summary_list.append(text)
    else:
        summary_list = filter(None, bill['summary'].split('■'))

    bill['summary_list'] = summary_list

    return render_template('post.html', bill=bill)
