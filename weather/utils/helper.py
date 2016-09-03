#!/usr/bin/env python
# -*- coding: utf-8 -*-

from datetime import date, datetime
import calendar
import requests
import json

from settings import API_GW_BASE_URL


def partial_by_index(list_object, index):
    def iter(l, result):
        if l == []:
            return result
        elif len(l) < index:
            result.append(l)
            return result

        result.append(l[:index])
        return iter(l[index:], result)

    return iter(list_object, [])


def map_weather_icons_css_with_weather_text():
    weather_icons = {
        '구름조금': 'wi-cloud',
        '구름많음': 'wi-cloudy',
        '흐림': 'wi-fog',
        '흐리고 비': 'wi-rain',
        '구름많고 비': 'wi-rain',
        '비': 'wi-rain',
        '소나기': 'wi-showers',
        '눈': 'wi-snow',
        '맑음': 'wi-day-sunny',
        'other': 'wi-cloud',
    }
    return weather_icons


def response_text_from_request(base_url, resource):
    text = ''

    try:
        response = requests.get(base_url+resource)
    except requests.ConnectionError:
        text = '{"status": 500, "exception": "ConnectionError"}'
    else:
        text = response.text

    if text.startswith('{}'):
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
        is_message = objects.get('message')
        if is_status and (is_exception or is_message):
            result = True

    return result


def get_status_code_if_error_in_objects(objects):
    if is_error_in_objects(objects):
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


def get_weather_objects(date=''):
    '''
    It evaluates today publish or specific day publish. It specifiies resource
    using date
    '''

    def get_publish_resources(date):
        publish_weather_resource = '/weather/today/weather/'
        publish_resource = '/weather/today/'

        if date != '':
            publish_weather_resource = '/weather/%s/weather/' % date
            publish_resource = '/weather/%s/' % date
        return publish_weather_resource, publish_resource

    publish_weather_resource, publish_resource = get_publish_resources(date)

    objects = dict()

    publish_weather = objects_from_request(API_GW_BASE_URL,
        publish_weather_resource)
    if is_error_in_objects(publish_weather):
        return publish_weather

    publish = objects_from_request(API_GW_BASE_URL, publish_resource)
    if is_error_in_objects(publish):
        return publish

    '''
    weather cities are seperated by 7.
    for example,
    weather[0:7] is seoul weekdays weather
    '''
    num_weekdays = 7
    partial_publish_weather = partial_by_index(publish_weather,
        num_weekdays)

    first_date = datetime.strptime(publish_weather[0]['date'], '%Y-%m-%d')

    first_weekday = first_date.weekday()

    weekdays = calendar.day_abbr[first_weekday:] +\
        calendar.day_abbr[:first_weekday]

    objects['partial_weather'] = partial_publish_weather
    objects['publish'] = publish
    objects['first_weekday'] = weekdays[0]
    objects['weekdays'] = weekdays
    objects['main_weather'] = publish_weather[0]
    objects['weather_icons'] = map_weather_icons_css_with_weather_text()

    return objects
