# -*- coding: utf-8 -*-
import datetime as dt

from flask_login import UserMixin
from sqlalchemy.orm import relationship, backref

from gamecenter.core.models import (
    DB as db,
    SurrogatePK,
    ReferenceCol,
    CRUDMixin
)
from gamecenter.extensions import bcrypt


class Role(SurrogatePK, db.Model):
    __tablename__ = 'roles'
    name = db.Column(db.String(80), nullable=False)
    user_id = ReferenceCol('users', nullable=True)
    user = db.relationship('User', backref='roles')

    def __init__(self, name, **kwargs):
        db.Model.__init__(self, name=name, **kwargs)

    def __repr__(self):
        return '<Role({name})>'.format(name=self.name)


class User(UserMixin, CRUDMixin, SurrogatePK, db.Model):
    __tablename__ = 'users'
    username = db.Column(db.String(80), unique=True, nullable=False)
    #: The hashed password
    password = db.Column(db.String(128), nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    active = db.Column(db.Boolean(), default=False)
    is_admin = db.Column(db.Boolean(), default=False, nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("games.id"), nullable=False)
    game = relationship("Game", backref=backref("requests"))

    def __init__(self, username, password=None, **kwargs):
        db.Model.__init__(self, username=username, **kwargs)
        if password:
            self.set_password(password)
        else:
            self.password = None

    def set_password(self, password):
        self.password = bcrypt.generate_password_hash(password)

    def check_password(self, value):
        return bcrypt.check_password_hash(self.password, value)

    def __repr__(self):
        return '<User({username!r})>'.format(username=self.username)
