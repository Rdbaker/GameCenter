# -*- coding: utf-8 -*-
"""A file for some utillity functions and classes."""


class InvalidUsage(Exception):
    """A handy class for notifying clients when things go wrong"""

    def __init__(self, message, status_code=400, payload=None):
        Exception.__init__(self)
        self.message = message
        self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """A function to serialize the object to a dict"""
        result = dict(self.payload or ())
        result['message'] = self.message
        return result
