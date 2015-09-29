# -*- coding: utf-8 -*-
import os

os_env = os.environ


class Config(object):
    # TODO: Change me
    SECRET_KEY = os_env.get('GAMECENTER_SECRET', 'secret-key')
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    JSONSCHEMA_DIR = os.path.join(PROJECT_ROOT, 'schemas')
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.


class ProdConfig(Config):
    """Production configuration."""
    ENV = 'prod'
    DEBUG = False
    # TODO: Change me
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'
    DEBUG_TB_ENABLED = False


class DevConfig(Config):
    """Development configuration."""
    SQLALCHEMY_DATABASE_URI = 'postgresql://localuser:localpassword@localhost/gamecenter'
    ENV = 'dev'
    DEBUG = True
    DEBUG_TB_PROFILER_ENABLED = True
    DB_NAME = 'dev.db'
    # Put the db file in project root
    DB_PATH = os.path.join(Config.PROJECT_ROOT, DB_NAME)
    DEBUG_TB_ENABLED = True
    ASSETS_DEBUG = True
    CACHE_TYPE = 'simple'


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
