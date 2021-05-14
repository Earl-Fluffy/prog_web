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
tagsSet = files.list_tags()


@app.route('/')
@app.route('/index')
def index():
    keys = files.keys()
    metadatas = [files.metadata(key) for key in keys]
    tags = request.args.get('pattern', '').split(" ")
    print(tags)
    if tags[0] != '':
        for tag in tags:
            metadatas = [metadata for metadata in metadatas
                         if tag in metadata["tags"]]
    metadatas = sorted(metadatas,
                       key=lambda x: x["id"],
                       reverse=True)
    context = {"imgs": metadatas,
               "tags": list(tagsSet),
               "nb_imgs": len(metadatas)}
    return render_template('index.html',
                           context=context)


@app.route('/<key>', methods=["GET", "POST"])
@app.route('/img/<key>', methods=["GET", "POST"])
def img(key):
    global tagsSet
    if request.method == "POST":
        new_tag = request.form['newtag'].replace(' ', '_')
        files.add_tag(key, new_tag)
        if new_tag not in tagsSet:
            tagsSet.add(new_tag)
            tagsSet = files.update_tagSet(tagsSet, new_tag)
    context = files.metadata(key)
    users = files.getUsers()
    context = {"metadata": files.metadata(key),
               "tags": list(tagsSet),
               "favUsers": [user for user in users
                            if int(key) in users[user]["favorites"]]}
    #favUsers = []
    #for user in context["users"]:
        #if int(key) in user["favorites"]:
            #favUsers.append(user["Username"])
    return render_template('img.html', context=context)


@app.route('/users', methods=["GET", "POST"])
def users():
    if request.method == "POST":
        newUser = {"username": request.form["username"],
                   "age": int(request.form["age"])}
        files.add_user(newUser)
    users = files.getUsers().keys()
    context = {"users": users}
    return render_template('users.html', context=context)


@app.route('/about')
def about():
    return make_response("test", 418)
