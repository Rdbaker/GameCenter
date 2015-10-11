# -*- coding: utf-8 -*-
"""API models."""
import sqlalchemy as db
from gamecenter.core.models import Base


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
    user_id = db.Column(db.Integer, index=True, unique=False, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String, index=True)
    created_at = db.Column(db.DateTime, nullable=False)


class Game(Base):
    """
    :id: Game
    :description: A game that will be using the leaderboard api.
    :param integer game_id: The game's id.__
    :param string api_key: The api_key games use to talk to the api.
    """
    __tablename__ = "games"
    game_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    api_key = db.Column(db.String, index=False, unique=True, nullable=False)
