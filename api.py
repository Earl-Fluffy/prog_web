# coding: utf-8

from flask import request, abort, make_response, current_app
from flask import Blueprint, jsonify
import json
import files


SITE_API = Blueprint('api', __name__,)


@SITE_API.route('/api')
@SITE_API.route('/api/<key>')
def send_dic(key=None):
    keys = files.keys()
    if key is None:
        return jsonify(list(sorted(keys)))
    if key not in keys:
        return "key not found", 404
    return json.load(open(f"./tags/{key}.json", "r"))


# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
