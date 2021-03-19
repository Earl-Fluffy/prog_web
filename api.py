# coding: utf-8

from flask import request, abort, make_response, current_app
from flask import Blueprint, jsonify

# Database access
from dbmgmt import get_users, add_user, get_user, mod_user

SITE_API = Blueprint('api', __name__,)


@SITE_API.route('/api')
@SITE_API.route('/api/<string:node0>', methods=['GET', 'POST'])
def api(node0=None):
    current_app.logger.debug('Looking at "{}" resource'.format(node0))
    abort(501)


# VIM MODLINE
# vim: ai ts=4 sw=4 sts=4 expandtab fileencoding=utf8
