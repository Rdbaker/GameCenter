# -*- coding: utf-8 -*-
"""API section."""
import datetime
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
@handle_api_key
@get_request_args
def leaderboards_controller(args):
    if request.method == 'GET':
        return get_paginated_scores(args)
    else:
        return jsonify(data=SCORESCHEMA.dump(create_entry()).data)


@blueprint.route('/add_score', methods=['POST'])
@handle_api_key
def add_score_controller():
    return jsonify(data=SCORESCHEMA.dump(create_entry()).data)


@blueprint.route('/add_score_and_list', methods=['POST'])
@handle_api_key
@get_request_args
def add_score_and_list_controller(args):
    new_score = create_entry()
    order = Score.score.desc()
    if args['sort'] == 'ascending':
        order = Score.score
    del args['user_id']  # we don't want to filter based on this
    args['end_date'] = datetime.datetime.utcnow()  # so that the end date is after the new score's date

    if args['filter_tag'] not in (None, args['tag']):
        raise InvalidUsage("filter_tag must be either null or the same as the new score's tag")

    if args['radius'] is None:
        raise InvalidUsage("radius is required")

    q = Score.query.order_by(order).filter(construct_and_(args))
    q_results = q.all()
    new_score_index = (i for i, row in enumerate(q_results) if row.id == new_score.id).next()

    offset = max(0, new_score_index - args['radius'])
    return scores_from_query(
        result_set=q.offset(offset).limit(2 * args['radius'] + 1),
        args=args,
    )


def get_paginated_scores(args):
    """Get a list of paginated scores."""
    order = Score.score.desc()
    if args['sort'] == 'ascending':
        order = Score.score
    res_set = Score.query.order_by(order).filter(construct_and_(args))
    return scores_from_query(
        result_set=res_set.offset(args['offset'] - 1).limit(args['page_size']),
        args=args,
        count=res_set.count()
    )


def create_entry():
    data = json.loads(request.data)
    data["game_id"] = g.game.id
    results, errors = SCORESCHEMA.load(data, session=SESSION)
    if errors:
        raise InvalidUsage(errors)

    DB.session.add(results)
    DB.session.commit()

    return results


def scores_from_query(result_set, args, count=None):
    res = [SCORESCHEMA.dump(score).data for score in result_set]
    if count is None:
        count = len(res)
    return jsonify(data=res, meta=get_meta_from_args(count, args))
