from flask.ext.testing import TestCase

from gamecenter.app import create_app
from gamecenter.settings import TestConfig


class BaseTestCase(TestCase):
    def create_app(self):
        app = create_app(config_object=TestConfig)
        return app
