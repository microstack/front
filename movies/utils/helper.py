#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import json

from settings import API_GW_BASE_URL


def response_text_from_request(base_url, resource):
    try:
        response = requests.get(base_url+resource)
    except requests.ConnectionError:
        error_log = 'ConnectionError'
        return

    text = response.text
    if text == '{}\n':
        text = '{"error": "no data"}'

    return text


def objects_from_request(base_url, resource):
    text = response_text_from_request(base_url, resource)
    objects = json.loads(text)
    return objects


def is_error_in_objects(objects):
    result = False
    if isinstance(objects, dict) and objects.get('error'):
        result = True

    return result


def get_error_type_if_error_in_objects(objects):
    if is_error_in_objects(objects):
        return objects['error']

    return None


def get_template_name_from_error_type(error_type, default):
    template_name = default

    if error_type == 'ConnectionError':
        template_name = 'error.html'
    if error_type == 'no data':
        template_name = 'no-data.html'

    return template_name


def get_template_name_from_objects_status(objects, default_template_name):
    error_type = get_error_type_if_error_in_objects(objects)
    template_name = get_template_name_from_error_type(error_type,
        default_template_name)
    return template_name


def get_movie_objects():
    objects = dict()

    latest_movies = objects_from_request(API_GW_BASE_URL, '/movies/latest/')
    if is_error_in_objects(latest_movies):
        data = get_error_type_if_error_in_objects(latest_movies)
        return latest_movies

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

    return objects
