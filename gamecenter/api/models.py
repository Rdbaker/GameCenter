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
    """
    __tablename__ = "scores"
    user_id = db.Column(db.Integer, index=True, unique=True, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    tag = db.Column(db.String, index=True)
    created_at = db.Column(db.DateTime, nullable=False)
