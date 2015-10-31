# -*- coding: utf-8 -*-
"""API section."""
import json

from flask import jsonify, request
from sqlalchemy.orm import scoped_session, sessionmaker

from . import blueprint
from gamecenter.api.models import Score
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


@blueprint.route('/leaderboards', methods=['GET', 'POST'])
@get_request_args
def leaderboards_controller(args):
    if request.method == 'GET':
        return get_paginated_scores(args)
    else:
        return create_entry()


@blueprint.route('/top', methods=['GET'])
def top():
    return jsonify({"meta": {"total": 10, "links":
                             {"next": "https://tmwild.com/api/top?offset=6&page_size=5"}}})


def get_paginated_scores(args):
    """Get a list of paginated scores."""
    order = Score.score.desc()
    if args['sort'] == 'ascending':
        order = Score.score
    return scores_from_query(
        Score
        .query
        .order_by(order)
        .filter(construct_and_(args))
        .offset(args['offset'] - 1)
        .limit(args['page_size']),
        args
    )


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


def scores_from_query(result_set, args):
    res = [SCORESCHEMA.dump(score).data for score in result_set]
    return jsonify(data=res, meta=get_meta_from_args(args))
