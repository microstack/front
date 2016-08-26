import requests
import os
import json

from flask import render_template
from flask import Flask

from settings import API_GW_BASE_URL

app = Flask(__name__)


def response_text_from_request(base_url, resource):
    response = requests.get(base_url + resource)
    text = response.text
    return text


@app.route('/movies/archive/')
def movie_archive():
    text = response_text_from_request(API_GW_BASE_URL, '/movies/')
    return text


@app.route('/movies/')
def movie_mainpage():
    latest_text = response_text_from_request(API_GW_BASE_URL,
        '/movies/latest/')
    latest_movies = json.loads(latest_text)

    grade_text = response_text_from_request(API_GW_BASE_URL, '/movies/grade/')
    high_grade_movies = json.loads(grade_text)

    '''
    It should loads thegenre movies for user selection using AJAX, later.
    But for now, it loads second query movies about genre.
    '''
    genres_text = response_text_from_request(API_GW_BASE_URL, '/movies/genres/')
    genres = json.loads(genres_text)
    genre = genres[1]['name']
    genre_movies_text = response_text_from_request(API_GW_BASE_URL,
        '/movies/genres/%s/' % genre)
    genre_movies = json.loads(genre_movies_text)

    return render_template('index.html', latest_movies=latest_movies,
        high_grade_movies=high_grade_movies, genre_movies=genre_movies,
        genre=genre)
