# -*- coding: utf-8 -*-
"""API models."""
import arrow
import sqlalchemy as db
from sqlalchemy.orm import relationship, backref

from rank.core.models import Base, CRUDMixin


class Score(Base):
    """
    :id: Score
    :description: An entry in the leaderboard database.
    :param integer user_id: The user's id for the leaderboard entry.
    :param integer score: The score for this leaderboard entry.
    :param string tag: An identifiable tag for this.
    :param datetime tag: The time the score was recorded.
    """
    __tablename__ = "scores"
    user_id = db.Column(db.Integer, index=True, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=lambda x: arrow.utcnow().datetime)

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    game = relationship("Game", backref=backref("scores"), cascade="delete-orphan, delete", single_parent=True)


class Game(Base, CRUDMixin):
    """
    :id: Game
    :description: A game that will be using the leaderboard api.
    :param string api_key: The api_key games use to talk to the api.
    """
    __tablename__ = "games"
    api_key = db.Column(db.String, index=True, unique=True, nullable=False)
    frozen = db.Column(db.Boolean, default=False, nullable=False)


class UserRequest(Base, CRUDMixin):
    """
    :id: UserRequest
    :description:
    :param datetime time_requested: The time the request was made
    :param int game_id: the game id to which the request belongs
    :param string http_verb: the verb with which the request was made
    :param string uri: the path of the request to the server
    :param int status: the integer response code sent to the client
    """
    __tablename__ = "requests"
    time_requested = db.Column(db.DateTime, nullable=False, default=lambda x: arrow.utcnow().datetime)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"))
    game = relationship("Game", backref=backref("user_requests"), cascade="delete-orphan, delete", single_parent=True)
    http_verb = db.Column(db.String, nullable=False)
    uri = db.Column(db.String, nullable=False)
    status = db.Column(db.Integer, nullable=False)
