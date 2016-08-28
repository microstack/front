#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from flask import render_template
from flask import Flask
app = Flask(__name__)

import requests

@app.route('/')
def index():

    '''
    서비스 목록 url을 받아서 http 요청이 성공하는지, 텍스트에 error가 포함되지
    않았는지 확인
    '''
    services = []
    for i in range(5):
        services.append(
            {
                'img_file': 'movies.png',
                'name': 'Micro Movie',
                'text': 'lorem lorem',
                'tag': 'Movie',
            })

    return render_template('index.html', services=services)
