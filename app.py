#!/usr/bin/env python3
# coding: utf-8

from flask import Flask, g
from flask import abort, request, make_response
from flask import render_template
from flask import json

import json as js
import files


# Set API dev in an another file
from api import SITE_API

## START: DO NOT MODIFY THIS PART ##
app = Flask(__name__,
            static_url_path="/static",
            static_folder="static")
# Add the API
app.register_blueprint(SITE_API)


@app.teardown_appcontext
def close_connection(exception):
    # manage database tear down
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
## END: DO NOT MODIFY THIS PART ##

# Get the tags list
tagsFile = open("static/tagsList.txt","r")
tagsList = [tag.rstrip("\n") for tag in tagsFile.read().split('\t')]
print(tagsList)

@app.route('/')
@app.route('/index')
@app.route('/index/<tag>')
def index(tag=None):
    keys = files.keys()
    context=[]
    print(tag)
    for key in keys:
        if not tag :
            context.append(files.tags(key))
        else:
            if tag in files.tags(key)['tags']:
                print('hey')
                context.append(files.tags(key))
    return render_template('index.html',context=context,tagsList=tagsList)

@app.route('/<key>')
@app.route('/img/<key>')
def img(key):
    context = files.tags(key)
    app.logger.debug(context)
    print(tagsList)
    return render_template('img.html', context=context,tagsList=tagsList)

@app.route('/about')
def about():
    return make_response("test", 418)
