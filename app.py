#!/usr/bin/env python3
# coding: utf-8

from flask import Flask, g
from flask import abort, request, make_response, redirect, url_for
from flask import render_template
from flask import json

import json as js
import files
import os


# Set API dev in an another file
from api import SITE_API

## START: DO NOT MODIFY THIS PART ##
app = Flask(__name__,
            static_url_path="/static",
            static_folder="static")
app.config['UPLOAD_FOLDER'] = "./static/imgs"
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


@app.route('/', methods=["GET", "POST"])
@app.route('/index', methods=["GET", "POST"])
def index():
    keys = files.keys()
    
    if request.method == "POST" and request.files['new_img'].filename != '':
        new_img = request.files['new_img']
        key = format(int(max(keys))+1, '06d')
        keys.add(key)
        ftype = new_img.filename.split(".")[1]
        filename = f"{key}.{ftype}"
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        new_img.save(path)
        files.addTagFile(filename)

    metadatas = [files.metadata(key) for key in keys]
    tags = request.args.get('pattern', '').split(" ")
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

    if key not in files.keys():
        return make_response("404 Image not found", 404)

    context = files.metadata(key)
    users = files.getUsers()
    favUsers = []
    otherUsers = []
    for user in users:
        if int(key) in users[user]["favorites"]:
            favUsers.append(user)
        else:
            otherUsers.append(user)
    context = {"metadata": files.metadata(key),
               "tags": list(tagsSet),
               "favUsers": favUsers,
               "otherUsers": otherUsers}
    return render_template('img.html', context=context)


@app.route('/fav_user/<key>', methods=["POST"])
def fav_user(key):
    favUser = request.form.get("newfav")
    app.logger.debug(key)
    app.logger.debug(favUser)

    if favUser != "":
        files.add_fav(favUser, int(key))
    return redirect(url_for('img', key=key), code=303)


@app.route('/users', methods=["GET", "POST"])
def users():
    if request.method == "POST":
        newUser = {"username": request.form["username"],
                   "age": int(request.form["age"])}
        files.add_user(newUser)
    users = files.getUsers().keys()
    context = {"users": users}
    return render_template('users.html', context=context)


@app.route('/users/<username>')
def user(username):
    users = files.getUsers()
    if username in users:
        user = users[username]
        user["found"] = True
        user["username"] = username
        user["favorites"] = [files.metadata(key) for key in user["favorites"]]
    else:
        user = {"found": False}
    context = {"tags": list(tagsSet)}
    return render_template('user.html', user=user, context=context)


@app.route('/about')
def about():
    return make_response("test", 418)
