#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from utils import get_available_services_info

import requests
from flask import render_template
from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():

    '''
    서비스 목록 url을 받아서 http 요청이 성공하는지, 텍스트에 error가 포함되지
    않았는지 확인
    '''
    available_services_info = get_available_services_info()

    return render_template('index.html',
        available_services_info=available_services_info)
