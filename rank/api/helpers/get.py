# -*- coding: utf-8 -*-
"""API helpers for GET requests."""
from datetime import datetime as dt
from functools import wraps
import json

import iso8601
from flask import request, g
from sqlalchemy import and_, or_

from rank.core.utils import InvalidUsage
from rank.api.models import Score

DEFAULTS = {
    'page_size': 5,
    'offset': 1,
    'sort': 'descending',
    'start_date': dt.fromtimestamp(0),
    'end_date': dt.utcnow,
    'radius': 12,
}


def construct_and_(args):
    """Construct the 'and_' clause for a sqlalchemy query"""
    conditions = [
        Score.game == g.game,
        Score.created_at >= args['start_date'],
        Score.created_at <= args['end_date']
    ]
    if args.get('tag') is not None:
        conditions.append(Score.tag == args['tag'])
    if args.get('user_id') is not None:
        conditions.append(or_(*[Score.user_id == u_id for u_id in args['user_id']]))
    return and_(*conditions)


def get_request_args(view_func):
    """Make sure all URL and POST data arguments are passed to a view."""
    @wraps(view_func)
    def get_args():
        """Get the URL and POST data arguments from a request."""
        both = {k: v[0] for k,v in dict(request.args).iteritems()}
        try:
            both.update(json.loads(request.data or "{}"))
        except:
            raise InvalidUsage('Malformed JSON received.')
        args = {}
        compare_dates(start=both.get('start_date'), end=both.get('end_date'))
        args['start_date'] = valid_start_date(both.get('start_date'))
        args['filter_tag'] = valid_tag(both.get('filter_tag'))
        args['page_size'] = valid_page_size(both.get('page_size'))
        args['end_date'] = valid_end_date(both.get('end_date'))
        args['user_id'] = valid_user_id(both.get('user_id'))
        args['radius'] = valid_radius(both.get('radius'))
        args['offset'] = valid_offset(both.get('offset'))
        args['sort'] = valid_sort(both.get('sort'))
        args['tag'] = valid_tag(both.get('tag'))
        return view_func(args)
    return get_args


def compare_dates(start, end):
    try:
        if start is None:
            start = DEFAULTS['start_date'].replace(tzinfo=None)
        else:
            start = iso8601.parse_date(start).replace(tzinfo=None)
        if end is None:
            end = DEFAULTS['end_date']().replace(tzinfo=None)
        else:
            end = iso8601.parse_date(end).replace(tzinfo=None)
        if end < start:
            raise InvalidUsage("The end_date argument must be a date after the start_date argument.")
    except iso8601.iso8601.ParseError:
        # This will be caught later
        pass


def valid_tag(tag):
    """Returns the given tag as a string"""
    if tag is not None:
        return str(tag)


def valid_radius(radius):
    """Returns the given radius as an integer"""
    try:
        if radius is not None:
            radius = int(radius)
            return min(radius, 12)
        else:
            return None
    except TypeError:
        raise InvalidUsage("The radius argument must be of type integer.")


def valid_user_id(user_id):
    """Returns the given user id as an integer array"""
    try:
        if user_id is not None:
            return [int(id) for id in str(user_id).split(',')]
    except TypeError:
        raise InvalidUsage("The user_id argument must be of type integer.")


def valid_end_date(date):
    """Returns the given date in datetime obj or returns the default"""
    try:
        if date is None:
            date = DEFAULTS['end_date']().replace(tzinfo=None).isoformat()
        return iso8601.parse_date(date).replace(tzinfo=None)
    except iso8601.iso8601.ParseError:
        raise InvalidUsage("The end_date argument must be a string in iso8601 date format.")


def valid_start_date(date):
    """Returns the given date in datetime obj or returns the default"""
    try:
        if date is None:
            date = DEFAULTS['start_date'].replace(tzinfo=None).isoformat()
        return iso8601.parse_date(date).replace(tzinfo=None)
    except iso8601.iso8601.ParseError:
        raise InvalidUsage("The start_date argument must be a string in iso8601 date format.")


def valid_sort(sort):
    """Returns the sort direction if it's valid, else returns the default"""
    if sort == 'ascending':
        return sort
    else:
        return DEFAULTS['sort']


def valid_offset(offset):
    """Returns the page offset if it's valid, else returns the default"""
    if offset is None:
        return DEFAULTS['offset']
    if isinstance(offset, unicode) and int(offset) > 0:
        return int(offset)
    else:
        raise InvalidUsage("The offset argument must be a positive integer.")


def valid_page_size(size):
    """Returns the given size if it's valid, else returns the default"""
    if isinstance(size, unicode) and int(size) >= 0:
        if int(size) >= 25:
            return 25  # TODO: factor out magick numbers
        else:
            return int(size)
    else:
        return DEFAULTS['page_size']
