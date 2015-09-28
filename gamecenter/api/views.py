# -*- coding: utf-8 -*-
"""API section."""
from flask import jsonify, request
from . import blueprint


@blueprint.route('/leaderboards')
def leaderboards_controller():
    if request.method == 'GET':
        return get_entries(request)
    elif request.method == 'POST':
        return create_entry(request)
    else:
        # return a 405 METHOD NOT ALLOWED
        return jsonify("")


def get_entries(request):
    return jsonify(scores='leaderboard entries')


def create_entry(request):
    return jsonify(message='congrats on the new entry')
