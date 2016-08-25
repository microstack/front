import os

from flask import render_template
from flask import Flask
app = Flask(__name__)

import requests

@app.route('/')
def index():
    services = []
    for i in range(5):
        services.append(
            {
                'img_file': 'movies.png',
                'name': 'Micro Movie',
                'text': 'lorem lorem'
            })

    return render_template('index.html', services=services)
