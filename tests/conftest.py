# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""
import pytest
from webtest import TestApp

from gamecenter.settings import TestConfig
from gamecenter.app import create_app
from gamecenter.database import db as _db


@pytest.yield_fixture(scope='function')
def app():
    _app = create_app(TestConfig)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture(scope='function')
def testapp(app):
    """A Webtest app."""
    return TestApp(app)


@pytest.yield_fixture(scope='function')
def db(app):
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    _db.drop_all()

"""Here's an example of how to tes up a test fixture
@pytest.fixture
def user(db):
    user = UserFactory(password='myprecious')
    db.session.commit()
    return user
"""
