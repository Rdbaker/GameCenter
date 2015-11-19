# -*- coding: utf-8 -*-
"""User section, including dashboard."""
import arrow
from flask import render_template, jsonify, g, redirect, url_for
from flask_login import login_required, current_user

from . import blueprint
from gamecenter.api.models import UserRequest, Score
from gamecenter.api.schema import UserRequestSchema, ScoreSchema
from gamecenter.api.views import handle_api_key, get_unique_key
from gamecenter.core.utils import InvalidUsage
from gamecenter.user.models import User
from gamecenter.user.schema import UserSchema

REQUESTSCHEMA = UserRequestSchema()
SCORESCHEMA = ScoreSchema()
USERSCHEMA = UserSchema()


@blueprint.route("/")
@login_required
def dashboard():
    if current_user.is_admin:
        midnight = arrow.utcnow().replace(hour=0, minute=0, second=0, microsecond=0).datetime
        daily_reqs = UserRequest.query.filter(UserRequest.time_requested > midnight).count()
        api_keys = User.query.filter(User.is_admin == False).count()
        return render_template("user/admin/dashboard.html",
                               api_keys=api_keys,
                               expected_reqs=(api_keys*3600),
                               user_requests=daily_reqs)
    else:
        return render_template("user/dashboard.html")


@blueprint.route("/settings")
@login_required
def settings():
    if current_user.is_admin:
        users = [USERSCHEMA.dump(user).data for user in User.query.filter(User.is_admin == False)]
        return render_template("user/admin/impersonate.html",
                               users=users)
    else:
        return render_template("user/settings.html")


@blueprint.route("/resetkey", methods=['POST'])
@login_required
def reset_key():
    game = current_user.game
    game.api_key = get_unique_key()
    game.save()
    return redirect(url_for('user.settings'))


@blueprint.route("/deleteuser/<id>", methods=['POST'])
@login_required
def delete_user(id):
    if not current_user.is_admin:
        raise InvalidUsage('Forbidden', status_code=403)
    if id == current_user.id:
        raise InvalidUsage("You can't delete yourself!")
    user = User.query.filter(User.id == id).first()
    user.delete()
    return redirect(url_for('user.settings'))


@blueprint.route("/togglefreeze/<user_id>", methods=['POST'])
@login_required
def freeze_user(user_id):
    if not current_user.is_admin:
        raise InvalidUsage('Forbidden', status_code=403)
    if user_id == current_user.id:
        raise InvalidUsage("You can't freeze yourself!")
    user = User.query.filter(User.id == user_id).first()
    user.game.frozen = not user.game.frozen
    user.game.save()
    return redirect(url_for('user.settings'))


@blueprint.route("/manage/<user_id>")
@login_required
def manage_data(user_id):
    user = current_user
    if user_id != user.id:
        if not current_user.is_admin:
            InvalidUsage("Forbidden", 403)
        user = User.get_by_id(user_id)
    return render_template(
        "user/managedata.html",
        scores=[SCORESCHEMA.dump(score).data for score in Score.query.filter(Score.game == user.game)])


@blueprint.route('/requests', methods=['GET'])
@handle_api_key
def requests_controller():
    weekly_reqs = [REQUESTSCHEMA.dump(req).data for req in current_user.requests_this_week()]
    daily_reqs = [REQUESTSCHEMA.dump(req).data for req in current_user.requests_today()]
    return jsonify(data={'weekly_reqs': weekly_reqs, 'daily_reqs': daily_reqs})
