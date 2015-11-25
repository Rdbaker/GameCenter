# -*- coding: utf-8 -*-
import os
import logging

os_env = os.environ


class Config(object):
    # TODO: Change this to be a better secret key (if we even need one)
    SECRET_KEY = os_env.get('GAMECENTER_SECRET', 'secret-key')
    HOST_URI = 'http://127.0.0.1:5000'
    APP_DIR = os.path.abspath(os.path.dirname(__file__))
    PROJECT_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    JSONSCHEMA_DIR = os.path.join(PROJECT_ROOT, 'schemas')
    ASSETS_DEBUG = False
    DEBUG_TB_ENABLED = False  # Disable Debug toolbar
    DEBUG_TB_INTERCEPT_REDIRECTS = False
    CACHE_TYPE = 'simple'  # Can be "memcached", "redis", etc.
    LOG_LEVEL = logging.INFO
    THROTTLE_LIMIT = 3600


class ProdConfig(Config):
    """Production configuration."""
    HOST_URI = 'https://tmwild.com'
    ENV = 'prod'
    DEBUG = False
    # TODO: Change this to an os_env.get type thing to hide our DB URI
    SQLALCHEMY_DATABASE_URI = 'postgresql://localhost/example'
    DEBUG_TB_ENABLED = False
    LOG_FILE = 'logs/prod_log.json'
    ERR_LOG = 'logs/prod_err_log.json'


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
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = 'logs/dev_log.json'
    ERR_LOG = 'logs/dev_err_log.json'


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'postgresql://localuser:localpassword@localhost/gamecenter_test'
    BCRYPT_LOG_ROUNDS = 1  # For faster tests
    WTF_CSRF_ENABLED = False  # Allows form testing
    LOG_LEVEL = logging.DEBUG
    LOG_FILE = 'logs/test_log.json'
    ERR_LOG = 'logs/test_err_log.json'
