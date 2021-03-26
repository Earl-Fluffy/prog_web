#!/usr/bin/env python3
# coding: utf-8

from flask import Flask, g
from flask import abort, request, make_response
from flask import render_template
from flask import json

import json as js


# Set API dev in an another file
from api import SITE_API

## START: DO NOT MODIFY THIS PART ##
app = Flask(__name__)
# Add the API
app.register_blueprint(SITE_API)


@app.teardown_appcontext
def close_connection(exception):
    # manage database tear down
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
## END: DO NOT MODIFY THIS PART ##


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/<key>')
@app.route('/img/<key>')
def img(key):
    context = {"id": format(int(key), '06d')}
    app.logger.debug(context["id"])
    return render_template('img.html', context=context)

@app.route('/about')
def about():
    return make_response("test", 418)
