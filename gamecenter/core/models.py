# -*- coding: utf-8 -*-
"""core models."""

from flask.ext.sqlalchemy import SQLAlchemy

DB = SQLAlchemy()


class Base(DB.Model):
    """
    This class extends the base Model from SQLAlchemy
    """
    __abstract__ = True
    id = DB.Column(DB.Integer, primary_key=True)
    created_at = DB.Column(DB.DateTime(), default=DB.func.now())


def init_db():
    import gamecenter.models
    DB.create_all()

def drop_db():
    import gamecenter.models
    DB.drop_all()
