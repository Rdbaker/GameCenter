# -*- coding: utf-8 -*-
from collections import OrderedDict
import json
import logging

import arrow
from flask import request, g

from rank.api.models import UserRequest


class RankTimedRotatingFileHandler(logging.handlers.TimedRotatingFileHandler):
    """
    Handles our log with care so the poor child knows where to go

    It will change what is appended to the filename based on the time it's rotated.
    Suffixes will appear in the form %Y-%m-%d E.g.:
    /var/log/rank/log-2015-11-04

    Every midnight, the logs rotate to a new file
    """
    def __init__(self, filename, backupCount=0, encoding=None, delay=False):
        kwargs = {
            'filename': filename,
            'backupCount': backupCount,
            'encoding': encoding,
            'delay': delay,
            'utc': True,
            'when': 'midnight',
            'interval': 1
            }
        super(RankTimedRotatingFileHandler, self).__init__(**kwargs)


class RankFormatter(logging.Formatter):
    """Wrap our logs in some nice JSON wrapping paper"""
    def format(self, record):
        """Format the record to be how we want it"""
        message = OrderedDict([
            ('time requested', arrow.utcnow().format()),
            ('game id', g.game.id),
            ('HTTP verb', request.method),
            ('uri', request.path),
            ('status', record.msg)
            ])
        # make a new UserRequest object here
        UserRequest.create(
            http_verb=request.method,
            game_id=g.game.id,
            status=record.msg,
            uri=request.path,
        )
        record.msg = json.dumps(message)
        return super(RankFormatter, self).format(record)


class RankErrFormatter(logging.Formatter):
    """Wrap our error logs in a nice output"""
    def format(self, record):
        """Format the record to be how we want it"""
        message = OrderedDict([
            ('time requested', arrow.utcnow().format()),
            ('trace', record.msg)
            ])
        record.msg = json.dumps(message)
        return super(RankErrFormatter, self).format(record)


class RankFilter(logging.Filter):
    """
    This filter does filter things
    """
    def filter(self, record):
        """Filter out requests that don't hit the API"""
        return '/api' in request.path


class RankErrFilter(logging.Filter):
    """
    Filters out non-exception traceback things
    """
    def filter(self, record):
        return record.level >= logging.ERROR
