# -*- coding: utf-8 -*-
"""API section."""
import json

from flask import jsonify, request
from sqlalchemy.orm import scoped_session, sessionmaker

from . import blueprint
from models import Score
from schema import ScoreSchema
from gamecenter.core.models import DB
from gamecenter.core.utils import InvalidUsage

session = scoped_session(sessionmaker())
score_schema = ScoreSchema()


@blueprint.route('/leaderboards', methods=['GET', 'POST'])
def leaderboards_controller():
    if request.method == 'GET':
        return get_entries()
    else:
        return create_entry()


@blueprint.route('/top', methods=['GET'])
def top():
    return jsonify({"meta": {"total": 10, "links":
                             {"next": "https://tmwild.com/api/top?offset=6&page_size=5"}}})


def get_entries():
    """Get the leaderboard entries for a user"""
    user_id = request.args.get('user_id')
    if user_id is None:
        return get_top_n()
    else:
        radius = request.args.get('radius')
        if radius is not None:
            return user_and_radius(user_id, radius)
        else:
            return list_of_user_scores(user_id)


def create_entry():
    results, errors = score_schema.load(json.loads(request.data),
                                        session=session)
    if errors:
        raise InvalidUsage(errors)

    DB.session.add(results)
    DB.session.commit()

    return jsonify(entry=score_schema.dump(results).data)


def get_top_n(n=10):
    """Get the top n scores."""
    n_limit = request.args.get('top_n')

    if n_limit is not None:
        n = n_limit

    return scores_from_query(
            Score.query.order_by('score desc').limit(n))


def list_of_user_scores(user_id):
    """Get the list of user's scores based on the id."""
    return scores_from_query(
            Score.query.filter(Score.user_id == user_id).all())


def user_and_radius(user_id, radius):
    # TODO: make this different from list_of_user_scores later
    return scores_from_query(
            Score.query.filter(Score.user_id == user_id).all())


def scores_from_query(result_set):
    res = [score_schema.dump(score).data for score in result_set]
    return jsonify(scores=res)
