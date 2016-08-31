#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import os
import json

from flask import render_template
from flask import Flask

from utils.helper import get_movie_objects,\
    get_template_name_from_objects_status
from settings import API_GW_BASE_URL

app = Flask(__name__)


@app.route('/movies/')
def movie_mainpage():
    objects = get_movie_objects()
    template_name = get_template_name_from_objects_status(objects,
        'index.html')

    return render_template(template_name, objects=objects)
