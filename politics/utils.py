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


def get_bill_list_object(resource):
    objects = dict()

    items = objects_from_request(API_GW_BASE_URL, resource)
    if is_error_in_objects(items):
        return items

    objects['bill_list'] = items['items']

    return objects


def get_bill_detail_object(resource):
    objects = dict()

    objects['bill'] = objects_from_request(API_GW_BASE_URL, resource)
    if is_error_in_objects(objects['bill']):
        return objects['bill']

    objects['bill']['summary_list'] = []

    if objects['bill'].get('summary') is None:
        text = '해당 의안에 대한 정보는 준비중입니다.'
        objects['bill']['summary_list'].append(text)
    else:
        '''
        API uses '■' as a delimeter for summary data.
        '''
        objects['bill']['summary_list'] = \
            filter(None, objects['bill']['summary'].split('■'))

    return objects
