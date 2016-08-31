import os
import requests
import json

from settings import API_GW_BASE_URL, SERVICE_MOVIE_RESOURCE,\
    SERVICE_POLITICS_RESOURCE, SERVICE_MOVIE_NAME, SERVICE_POLITICS_NAME


movies_info = {
    'img_file': 'movies.png', 'name': 'Micro Movie', 'text': 'lorem lorem',
    'tag': 'Movie'
}

politics_info = {
    'img_file': 'politics.png', 'name': 'Micro Politics',
    'text': 'lorem lorem', 'tag': 'Politics'
}

weather_info = {
    'img_file': 'weather.png', 'name': 'Micro Weather',
    'text': 'lorem lorem', 'tag': 'Weather'
}

services_info = [
    movies_info,
    politics_info,
    weather_info
]

'''
"""
Getting the available service info's takes a long time. And it takes more when
it is realtime. Therefore it is skipped for now.
"""
service_data = [
    (SERVICE_MOVIE_NAME, SERVICE_MOVIE_RESOURCE),
    (SERVICE_POLITICS_NAME, SERVICE_POLITICS_RESOURCE)
]


def get_services(service_data):

    def get_service_url(resource):
        return API_GW_BASE_URL + resource

    def get_service_dict(service_name, resource):
        return {service_name: get_service_url(resource)}

    services = dict()
    for name, resource in service_data:
        service = get_service_dict(name, resource)
        services.update(service)
    return services


def get_available_services(service_data=service_data):
    available_services = []
    
    services = get_services(service_data)
    for key in services.keys():
        try:
            response = requests.get(services[key])
        except requests.ConnectionError:
            continue
 
        if response.status_code == 200:
            text = response.text
            if text.startswith('{"error":'):
                continue

        available_services.append(key)
    
    return available_services


def get_available_services_info(services_info=services_info):
    available_services_info = []
    services = get_available_services()
    for service in services:
        available_services_info.append(services_info[service])

    return available_services_info
'''
