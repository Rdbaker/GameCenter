#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
from flask_script import Manager, Shell, Server
from flask_script.commands import Clean, ShowUrls
from flask_migrate import MigrateCommand, Migrate
from flask.ext.sqlalchemy import sqlalchemy

from gamecenter.app import create_app
from gamecenter.settings import DevConfig, ProdConfig
from gamecenter.core.models import Base, DB

DEFAULT_DB = 'postgres'
CREATE_DB = 'create database %s'

if os.environ.get("GAMECENTER_ENV") == 'prod':
    application = create_app(ProdConfig)
else:
    application = create_app(DevConfig)

HERE = os.path.abspath(os.path.dirname(__file__))
TEST_PATH = os.path.join(HERE, 'tests')

migrate = Migrate(application, Base)
manager = Manager(application)


def _make_context():
    """Return context dict for a shell session so you can access
    app, db, and the User model by default.
    """
    return {'app': application, 'db': DB}


@manager.command
def test():
    """Run the tests."""
    import pytest
    exit_code = pytest.main([TEST_PATH, '--verbose'])
    return exit_code


@manager.command
def setup_db():
    """Set up the local and test databases."""
    (base_uri, local_db) = application.config['SQLALCHEMY_DATABASE_URI'].rsplit('/', 1)
    engine = sqlalchemy.create_engine('/'.join([base_uri, DEFAULT_DB]))
    conn = engine.connect()
    conn.execute('commit')
    conn.execute(CREATE_DB % local_db)
    conn.execute('commit')
    test_db = local_db + '_test'
    conn.execute(CREATE_DB % test_db)
    conn.close()


manager.add_command('server', Server())
manager.add_command('shell', Shell(make_context=_make_context))
manager.add_command('db', MigrateCommand)
manager.add_command("urls", ShowUrls())
manager.add_command("clean", Clean())

if __name__ == '__main__':
    manager.run()
