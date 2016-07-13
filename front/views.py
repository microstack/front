from flask import render_template

from . import app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/movies/')
def movie_mainpage():
    return 'Movie mainpage'

@app.route('/actors/')
def actor_mainpage():
    return 'Actor mainpage'
