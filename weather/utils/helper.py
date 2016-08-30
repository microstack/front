from datetime import date, datetime
import calendar
import requests
import json

from settings import API_GW_BASE_URL


def partial_by_index(list_object, index):
    def iter(l, result):
        if l == []:
            return result
        result.append(l[:index])
        return iter(l[index:], result)

    return iter(list_object, [])


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


def get_weather_objects(date=''):
    def get_publish_resources(date):
        publish_weather_resource = '/weather/today/weather/'
        publish_resource = '/weather/today/'

        if date != '':
            publish_weather_resource = '/weather/publishes/%s/weather/' % date
            publish_resource = 'weather/publishes/%s/' % date
        return publish_weather_resource, publish_resource

    publish_weather_resource, publish_resource = get_publish_resources(date)

    objects = dict()

    publish_weather = objects_from_request(API_GW_BASE_URL,
        publish_weather_resource)

    '''
    weather cities are seperated by 7.
    for example,
    weather[0:7] is seoul weekdays weather
    '''
    num_weekdays = 7
    partial_publish_weather = partial_by_index(publish_weather,
        num_weekdays)

    publish = objects_from_request(API_GW_BASE_URL, publish_resource)

    first_date = datetime.strptime(publish_weather[0]['date'], '%Y-%m-%d')

    first_weekday = first_date.weekday()

    weekdays = calendar.day_abbr[first_weekday:] +\
        calendar.day_abbr[:first_weekday]

    objects['partial_weather'] = partial_publish_weather
    objects['publish'] = publish
    objects['first_weekday'] = weekdays[0]
    objects['weekdays'] = weekdays
    objects['main_weather'] = publish_weather[0]

    return objects
