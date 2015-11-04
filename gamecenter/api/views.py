# -*- coding: utf-8 -*-
"""API section."""
import functools
import json
import random
import string

from flask import jsonify, request, g
from sqlalchemy.orm import scoped_session, sessionmaker

from . import blueprint
from gamecenter.api.models import Score, Game
from gamecenter.api.schema import ScoreSchema
from gamecenter.core.models import DB
from gamecenter.core.utils import InvalidUsage
from gamecenter.api.helpers.meta import get_meta_from_args
from gamecenter.api.helpers.get import (
    get_request_args,
    construct_and_
)

SESSION = scoped_session(sessionmaker())
SCORESCHEMA = ScoreSchema()


def handle_api_key(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if "Authorization" in request.headers:
            api_key = request.headers["Authorization"][7:]  # from the string form "Bearer <api_key>"
        else:
            api_key = ""
        game = Game.query.filter(Game.api_key == api_key).first()
        if game:
            g.game = game
            return f(*args, **kwargs)
        else:
            raise InvalidUsage("Unable to authenticate you.", 401)
    return decorated_function


@blueprint.route('/signup', methods=['GET'])
def signup():
    chars = string.ascii_uppercase + string.digits
    length = 32

    key = ''.join(random.choice(chars) for _ in range(length))
    while Game.query.filter_by(api_key=key).first():
        key = ''.join(random.choice(chars) for _ in range(length))

    game = Game(api_key=key)
    DB.session.add(game)
    DB.session.commit()
    return jsonify({"data": {"api_key": key}})


@blueprint.route('/leaderboards', methods=['GET', 'POST'])
@get_request_args
def leaderboards_controller(args):
    if request.method == 'GET':
        return get_paginated_scores(args)
    else:
        return create_entry()


def get_paginated_scores(args):
    """Get a list of paginated scores."""
    order = Score.score.desc()
    if args['sort'] == 'ascending':
        order = Score.score
    res_set = Score.query.order_by(order).filter(construct_and_(args))
    return scores_from_query(
        result_set=res_set.offset(args['offset'] - 1).limit(args['page_size']),
        count=res_set.count(),
        args=args)


def create_entry():
    results, errors = SCORESCHEMA.load(json.loads(request.data),
                                       session=SESSION)
    if errors:
        raise InvalidUsage(errors)

    DB.session.add(results)
    DB.session.commit()

    return jsonify(entry=SCORESCHEMA.dump(results).data)


def user_and_radius(user_id, radius):
    # TODO: make this work
    return scores_from_query(
        Score.query.filter(Score.user_id == user_id).all())


def scores_from_query(result_set, count, args):
    res = [SCORESCHEMA.dump(score).data for score in result_set]
    return jsonify(data=res, meta=get_meta_from_args(count, args))
