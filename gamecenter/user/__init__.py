# -*- coding: utf-8 -*-
"""set up the user blueprint."""
from flask import Blueprint

blueprint = Blueprint('user', __name__, url_prefix="/dashboard", static_folder="../static")
