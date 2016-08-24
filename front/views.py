import os

from flask import render_template
from flask import Flask
app = Flask(__name__)

import requests

@app.route('/')
def index():
    return render_template('index.html')
