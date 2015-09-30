# -*- coding: utf-8 -*-
"""Core views."""
from flask import jsonify

from . import blueprint
from gamecenter import __version__


@blueprint.route('/status')
def status_reporter():
    # be sure to include the version in this later
    return jsonify(status="ok", version=__version__)
