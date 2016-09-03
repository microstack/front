#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import json

from settings import API_GW_BASE_URL


def response_text_from_request(base_url, resource):
    text = ''

    try:
        response = requests.get(base_url+resource)
    except requests.ConnectionError:
        text = '{"status": 500, "exception": "ConnectionError"}'
    else:
        text = response.text

    if text == '{}\n':
        text = '{"status": 404, "exception": "No resource"}'

    return text


def objects_from_request(base_url, resource):
    text = response_text_from_request(base_url, resource)
    try:
        objects = json.loads(text)
    except ValueError:
        objects = {"status": 500, "exception": "ValueError"}

    if isinstance(objects, dict):
        server_error_msg = "Internal Server Error"
        if objects.get("message") == server_error_msg:
            objects.update({"status": 500})

    return objects


def is_error_in_objects(objects):
    result = False
    if isinstance(objects, dict):
        is_status = objects.get('status')
        is_exception = objects.get('exception')
        if is_status and is_exception:
            result = True

    return result


def get_status_code_if_error_in_objects(objects):
    if is_error_in_objects(objects):
        status = objects.get("status")
        if not status:
            objects['status'] = 500
        return objects['status']

    return 200


def get_template_name_from_status_code(status_code, default):
    template_name = default

    if status_code == 500:
        template_name = 'exceptions/500.html'
    if status_code == 404:
        template_name = 'exceptions/404.html'

    return template_name


def get_template_name_from_objects_status(objects, default_template_name):
    status_code = get_status_code_if_error_in_objects(objects)

    template_name = get_template_name_from_status_code(status_code,
        default_template_name)
    return template_name


def get_movie_objects():
    objects = dict()

    latest_movies = objects_from_request(API_GW_BASE_URL, '/movies/latest/')
    if is_error_in_objects(latest_movies):
        return latest_movies

    high_grade_movies = objects_from_request(API_GW_BASE_URL,
        '/movies/grade/')
    if is_error_in_objects(high_grade_movies):
        return high_grade_movies

    '''
    It should loads thegenre movies for user selection using AJAX, later.
    But for now, it loads second query movies about genre.
    '''
    genre = '스릴러'
    genre_movies = objects_from_request(API_GW_BASE_URL,
        '/movies/genres/%s/' % genre)
    if is_error_in_objects(genre_movies):
        return genre_movies

    objects['latest_movies'] = latest_movies
    objects['high_grade_movies'] = high_grade_movies
    objects['genre_movies'] = genre_movies
    objects['genre'] = genre

    return objects
