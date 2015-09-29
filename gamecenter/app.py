# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
from flask import Flask, render_template, jsonify

from gamecenter.core.utils import InvalidUsage
from gamecenter.settings import ProdConfig
from gamecenter.assets import assets
from gamecenter.core.models import DB as db
from gamecenter.extensions import (
    cache,
    migrate,
    debug_toolbar,
)
from gamecenter.public import views as public
from gamecenter.api import views as api
from gamecenter.core import views as core


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_errorhandlers(app)
    register_blueprints(app)

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        """A handler for any endpoint that raises an InvalidUsage exception"""
        return jsonify(error.to_dict()), error.status_code

    return app


def register_extensions(app):
    assets.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    app.register_blueprint(public.blueprint)
    app.register_blueprint(api.blueprint)
    app.register_blueprint(core.blueprint)
    return None


def register_errorhandlers(app):
    def render_error(error):
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None
