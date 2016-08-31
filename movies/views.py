#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import json

from flask import render_template
from flask import Flask

from utils.helper import get_movie_objects, is_error_in_objects
from settings import API_GW_BASE_URL

app = Flask(__name__)


@app.route('/movies/archive/')
def movie_archive():
    text = response_text_from_request(API_GW_BASE_URL, '/movies/')
    return text


@app.route('/movies/')
def movie_mainpage():
    objects = get_movie_objects()

    if is_error_in_objects(objects):
        return render_template('error.html')

    return render_template('index.html', objects=objects)
