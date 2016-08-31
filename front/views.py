#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

from utils import services_info

import requests
from flask import render_template
from flask import Flask
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html', services_info=services_info)
