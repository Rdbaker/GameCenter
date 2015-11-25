# -*- coding: utf-8 -*-
"""The app module, containing the app factory function."""
import logging

from flask import (
    current_app,
    Flask,
    g,
    jsonify,
    render_template,
    request,
)

from rank.api import views as api
from rank.api.models import Game
from rank.assets import assets
from rank.core import views as core
from rank.core.models import DB as db
from rank.core.utils import InvalidUsage
from rank.extensions import (
    cache,
    login_manager,
    migrate,
    debug_toolbar,
)
from rank.logger import (
    RankErrFilter,
    RankErrFormatter,
    RankFilter,
    RankFormatter,
    RankTimedRotatingFileHandler,
)
from rank.public import views as public
from rank.settings import ProdConfig
from rank.user import views as user


def create_app(config_object=ProdConfig):
    """An application factory, as explained here:
        http://flask.pocoo.org/docs/patterns/appfactories/

    :param config_object: The configuration object to use.
    """
    app = Flask(__name__)
    app.config.from_object(config_object)

    register_logger(app)
    register_extensions(app)
    register_blueprints(app)
    register_errorhandlers(app)

    @app.errorhandler(InvalidUsage)
    def handle_invalid_usage(error):
        """A handler for any endpoint that raises an InvalidUsage exception"""
        return jsonify(error.to_dict()), error.status_code

    @app.after_request
    def log_request(resp):
        """
        Create the log to send to the rotated log file
        """
        current_app.logger.info(str(resp.status_code))
        return resp

    @app.before_request
    def throttle():
        """
        Throttle the request if need be
        """
        if api.blueprint.url_prefix not in request.path:
            # don't need to throttle these requests
            return None
        if "Authorization" not in request.headers:
            # let somebody else handle this situation
            return None
        api_key = request.headers["Authorization"][7:]  # from the string form "Bearer <api_key>"
        game = Game.query.filter(Game.api_key == api_key).first()
        if not game:
            # let somebody else handle this situation
            return None
        g.game = game
        if game.user.request_count_today() >= app.config['THROTTLE_LIMIT']:
            return handle_invalid_usage(InvalidUsage("Exceeded maximum API requests.", 429))

    return app


def register_extensions(app):
    """Register the extensiosn of the app"""
    assets.init_app(app)
    cache.init_app(app)
    db.init_app(app)
    login_manager.init_app(app)
    debug_toolbar.init_app(app)
    migrate.init_app(app, db)
    return None


def register_blueprints(app):
    """Register the routes of the app"""
    app.register_blueprint(public.blueprint)
    app.register_blueprint(api.blueprint)
    app.register_blueprint(core.blueprint)
    app.register_blueprint(user.blueprint)
    return None


def register_errorhandlers(app):
    """
    Set up the proper error handling things to do
    """
    def render_error(error):
        """
        Render the correct template based on the error code
        """
        # If a HTTPException, pull the `code` attribute; default to 500
        error_code = getattr(error, 'code', 500)
        return render_template("{0}.html".format(error_code)), error_code
    for errcode in [401, 404, 500]:
        app.errorhandler(errcode)(render_error)
    return None


def register_logger(app):
    """
    Initialize logging infrastructure based on the app environment
    """
    # remove the default handler
    app.logger.removeHandler(app.logger.handlers[0])
    # set the logger log level
    app.logger.setLevel(app.config['LOG_LEVEL'])

    # add a new handler and formatter to each of the loggers
    err_handler = RankTimedRotatingFileHandler(app.config['ERR_LOG'])
    err_handler.setLevel(logging.ERROR)
    err_handler.setFormatter(RankErrFormatter("%(message)s"))
    app.logger.addHandler(err_handler)
    err_handler.addFilter(RankErrFilter())

    handler = RankTimedRotatingFileHandler(app.config['LOG_FILE'])
    handler.setLevel(logging.DEBUG)
    handler.setFormatter(RankFormatter("%(message)s"))
    app.logger.addFilter(RankFilter())
    app.logger.addHandler(handler)
    return None
