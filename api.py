# coding: utf-8

from flask import request, abort, make_response, current_app
from flask import redirect, url_for
from flask import render_template
from flask import Blueprint, jsonify
import json
import files
import os


SITE_API = Blueprint('api', __name__,)
upload_folder = "./static/imgs"


@SITE_API.route('/api')
@SITE_API.route('/api/<key>')
def send_dic(key=None):
    keys = files.keys()
    if key is None:
        return jsonify(list(sorted(keys)))
    if key not in keys:
        return "key not found", 404
    return json.load(open(f"./tags/{key}.json", "r"))


@SITE_API.route('/api/upload', methods=["POST"])
def upload_img():
    if request.files['new_img'].filename != '':
        keys = files.keys()
        new_img = request.files['new_img']
        key = format(int(max(keys))+1, '06d')
        keys.add(key)
        ftype = new_img.filename.split(".")[1]
        filename = f"{key}.{ftype}"
        path = os.path.join(upload_folder, filename)
        new_img.save(path)
        files.addTagFile(filename)
    return redirect(url_for('index'), code=303)


@SITE_API.route('/api/<key>', methods=["POST"])
def add_tag(key):
    tagsSet = files.list_tags()
    new_tag = request.form['newtag'].replace(' ', '_')
    files.add_tag(key, new_tag)
    if new_tag not in tagsSet:
        tagsSet.add(new_tag)
        tagsSet = files.update_tagSet(tagsSet, new_tag)
    return redirect(url_for('img', key=key))


@SITE_API.route('/api/addfavimg/<key>', methods=["POST"])
def fav_user(key):
    favUser = request.form.get("newfav")
    if favUser != "":
        files.add_fav(favUser, int(key))
    return redirect(url_for('img', key=key), code=303)


@SITE_API.route('/api/addusr', methods=["POST"])
def add_user():
    if request.form["username"] != "":
        newUser = {"username": request.form["username"],
                   "age": int(request.form["age"])}
        files.add_user(newUser)
    return redirect(url_for('users'), code=303)

# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
