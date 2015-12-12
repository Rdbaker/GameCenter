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
from rank.api.models import Score, Game
from rank.api.schema import ScoreSchema, UserRequestSchema
from rank.core.models import DB
from rank.core.utils import InvalidUsage
from rank.api.helpers.meta import get_meta_from_args
from rank.api.helpers.get import (
    get_request_args,
    construct_and_
)

SESSION = scoped_session(sessionmaker())
SCORESCHEMA = ScoreSchema()
REQUESTSCHEMA = UserRequestSchema()


def handle_api_key(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if "Authorization" in request.headers:
            api_key = request.headers["Authorization"][7:]  # from the string form "Bearer <api_key>"
        else:
            api_key = ""
        game = Game.query.filter(Game.api_key == api_key).first()
        if game:
            if game.frozen:
                raise InvalidUsage("This account has been frozen.", 403)
            g.game = game
            return f(*args, **kwargs)
        else:
            raise InvalidUsage("Unable to authenticate you.", 401)
    return decorated_function


def create_game():
    game = Game(api_key=get_unique_key())
    DB.session.add(game)
    DB.session.commit()
    return game


def get_unique_key():
    chars = string.ascii_uppercase + string.digits
    length = 32

    key = ''.join(random.choice(chars) for _ in range(length))
    while Game.query.filter_by(api_key=key).first():
        key = ''.join(random.choice(chars) for _ in range(length))
    return key


@blueprint.route('/leaderboards', methods=['GET'])
@handle_api_key
@get_request_args
def leaderboards_controller(args):
    order = Score.score.desc()
    if args['sort'] == 'ascending':
        order = Score.score
    res_set = Score.query.order_by(order).filter(construct_and_(args))
    return scores_from_query(
        result_set=res_set.offset(args['offset'] - 1).limit(args['page_size']),
        args=args,
        endpoint='leaderboards',
        count=res_set.count(),
    )


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
        endpoint='add_score_and_list',
    )


def create_entry():
    try:
        data = json.loads(request.data)
    except:
        raise InvalidUsage('Malformed JSON')
    data["game_id"] = g.game.id
    results, errors = SCORESCHEMA.load(data, session=SESSION)
    if errors:
        raise InvalidUsage(errors)

    DB.session.add(results)
    DB.session.commit()

    return results


def scores_from_query(result_set, args, endpoint, count=None):
    res = [SCORESCHEMA.dump(score).data for score in result_set]
    if count is None:
        count = len(res)
    return jsonify(data=res, meta=get_meta_from_args(count, args, endpoint))
