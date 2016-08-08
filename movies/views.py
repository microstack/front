import requests
import os

from flask import render_template
from flask import Flask

from settings import API_GW_BASE_URL

def response_text_from_request(self, base_url, resource):
    response = requests.get(base_url + resource)
    text = response.text
    return text


@app.route('/movies/')
def movie_mainpage():
    text = response_text_from_request(API_GW_BASE_URL, '/movies/')
    return text
