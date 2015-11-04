# -*- coding: utf-8 -*-
"""API models."""
import datetime

import sqlalchemy as db
from sqlalchemy.orm import relationship, backref

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
    user_id = db.Column(db.Integer, index=True, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)

    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    game = relationship("Game", backref=backref("scores"))


class Game(Base):
    """
    :id: Game
    :description: A game that will be using the leaderboard api.
    :param string api_key: The api_key games use to talk to the api.
    """
    __tablename__ = "games"
    api_key = db.Column(db.String, index=False, unique=True, nullable=False)
