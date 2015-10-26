# -*- coding: utf-8 -*-
"""API helpers for GET requests."""
import iso8601
from flask import request
from datetime import datetime as dt
from sqlalchemy import and_

from gamecenter.api.models import Score

DEFAULTS = {
    'page_size': 5,
    'offset': 1,
    'sort': 'descending',
    'start_date': dt.fromtimestamp(0),
    'end_date': dt.utcnow()
    }


def construct_and_(args):
    """Construct the 'and_' clause for a sqlalchemy query"""
    if args['user_id'] is None:
        if args['tag'] is None:
            return and_(
                Score.created_at >= args['start_date'],
                Score.created_at <= args['end_date'])
        else:
            return and_(
                Score.created_at >= args['start_date'],
                Score.created_at <= args['end_date'],
                Score.tag == args['tag'])
    elif args['tag'] is None:
        return and_(
            Score.created_at >= args['start_date'],
            Score.created_at <= args['end_date'],
            Score.user_id == args['user_id'])
    else:
        return and_(
            Score.created_at >= args['start_date'],
            Score.created_at <= args['end_date'],
            Score.tag == args['tag'],
            Score.user_id == args['user_id'])


def get_request_args(view_func):
    """Make sure all arguments are passed to a view."""
    def get_args():
        """Get the arguments from a request."""
        args = {}
        args['start_date'] = valid_start_date(request.args.get('start_date'))
        args['page_size'] = valid_page_size(request.args.get('page_size'))
        args['end_date'] = valid_end_date(request.args.get('end_date'))
        args['user_id'] = valid_user_id(request.args.get('user_id'))
        args['offset'] = valid_offset(request.args.get('offset'))
        args['sort'] = valid_sort(request.args.get('sort'))
        args['tag'] = valid_tag(request.args.get('tag'))
        return view_func(args)
    return get_args


def valid_tag(tag):
    """Returns the given tag as a string"""
    if tag is not None:
        return str(tag)
    else:
        return tag


def valid_user_id(user_id):
    """Returns the given user id as an integer"""
    try:
        return int(user_id)
    except TypeError:
        return None


def valid_end_date(date):
    """Returns the given date in datetime obj or returns the default"""
    try:
        return iso8601.parse_date(date)
    except iso8601.iso8601.ParseError:
        return DEFAULTS['end_date']


def valid_start_date(date):
    """Returns the given date in datetime obj or returns the default"""
    try:
        return iso8601.parse_date(date)
    except iso8601.iso8601.ParseError:
        return DEFAULTS['start_date']


def valid_sort(sort):
    """Returns the sort direction if it's valid, else returns the default"""
    if sort == 'ascending':
        return sort
    else:
        return DEFAULTS['sort']


def valid_offset(offset):
    """Returns the page offset if it's valid, else returns the default"""
    if isinstance(offset, unicode) and int(offset) > 0:
        return int(offset)
    else:
        return DEFAULTS['offset']


def valid_page_size(size):
    """Returns the given size if it's valid, else returns the default"""
    if isinstance(size, unicode) and int(size) >= 0:
        if int(size) >= 25:
            return 25
        else:
            return int(size)
    else:
        return DEFAULTS['page_size']
