import requests
import json

from flask import render_template
from flask import Flask

from utils import get_bill_list_object, get_bill_detail_object,\
    get_template_name_from_objects_status

app = Flask(__name__)


@app.route('/politics/')
def bill_list():
    resource = '/politics/'
    objects = get_bill_list_object(resource)
    template_name = get_template_name_from_objects_status(objects,
        'index.html')
    return render_template(template_name, objects=objects)


@app.route('/politics/<string:id>/')
def bill_detail(id):
    resource = '/politics/%s' % id
    objects = get_bill_detail_object(resource)
    print(objects)
    template_name = get_template_name_from_objects_status(objects,
        'post.html')

    return render_template(template_name, objects=objects)
