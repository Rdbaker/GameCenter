# -*- coding: utf-8 -*-
"""User section, including dashboard."""
import datetime

import arrow
from flask import render_template, jsonify, g, redirect, url_for
from flask_login import login_required, current_user

from . import blueprint
from gamecenter.api.models import UserRequest, Score
from gamecenter.api.schema import UserRequestSchema, ScoreSchema
from gamecenter.api.views import handle_api_key, get_unique_key

REQUESTSCHEMA = UserRequestSchema()
SCORESCHEMA = ScoreSchema()


@blueprint.route("/")
@login_required
def dashboard():
    return render_template("user/dashboard.html")


@blueprint.route("/settings")
@login_required
def settings():
    return render_template("user/settings.html")


@blueprint.route("/resetkey", methods=['POST'])
@login_required
def reset_key():
    game = current_user.game
    game.api_key = get_unique_key()
    game.save()
    return redirect(url_for('user.settings'))


@blueprint.route("/manage")
@login_required
def manage_data():
    return render_template(
        "user/managedata.html",
        scores=[SCORESCHEMA.dump(score).data for score in Score.query.filter(Score.game == current_user.game)])


@blueprint.route('/requests', methods=['GET'])
@handle_api_key
def requests_controller():
    seven_days_ago = arrow.utcnow().date() - datetime.timedelta(days=7)
    yesterday = arrow.utcnow().date() - datetime.timedelta(days=1)
    weekly_reqs = UserRequest.query.filter(
        UserRequest.game_id == g.game.id,
        UserRequest.time_requested > seven_days_ago).order_by(UserRequest.time_requested.desc())
    daily_reqs = UserRequest.query.filter(
        UserRequest.game_id == g.game.id,
        UserRequest.time_requested > yesterday).order_by(UserRequest.time_requested.desc())
    weekly_reqs = [REQUESTSCHEMA.dump(req).data for req in weekly_reqs]
    daily_reqs = [REQUESTSCHEMA.dump(req).data for req in daily_reqs]
    return jsonify(data={'weekly_reqs': weekly_reqs, 'daily_reqs': daily_reqs})
