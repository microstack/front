#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
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


@app.route('/movies/archive/')
def movie_archive():
    text = response_text_from_request(API_GW_BASE_URL, '/movies/')
    return text


@app.route('/movies/')
def movie_mainpage():
    objects = dict()
    latest_movies = objects_from_request(API_GW_BASE_URL, '/movies/latest/')
    high_grade_movies = objects_from_request(API_GW_BASE_URL, 
        '/movies/grade/')

    '''
    It should loads thegenre movies for user selection using AJAX, later.
    But for now, it loads second query movies about genre.
    '''
    genre = '스릴러'
    genre_movies = objects_from_request(API_GW_BASE_URL,
        '/movies/genres/%s/' % genre)

    objects['latest_movies'] = latest_movies
    objects['high_grade_movies'] = high_grade_movies
    objects['genre_movies'] = genre_movies
    objects['genre'] = genre

    if is_error_in_objects(objects):
        return render_template('error.html')

    return render_template('index.html', objects=objects)
