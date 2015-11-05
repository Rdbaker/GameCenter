# -*- coding: utf-8 -*-
"""API helpers for META info."""
from flask import current_app


def get_meta_from_args(count, args):
    """Construct the meta dictionary from the args"""
    meta = {}
    uri = current_app.config['HOST_URI']
    offset = args['offset']
    page_size = args['page_size']
    meta['total'] = count
    meta['links'] = {}

    if offset + page_size < count:
        meta['links']['next'] = (uri + "/api/leaderboards?offset={0}&page_size={1}"
                                 .format(min(int(offset) + int(page_size), count),
                                         int(page_size)))
    if offset > 1:
        meta['links']['prev'] = (uri + "/api/leaderboards?offset={0}&page_size={1}"
                                 .format(max(int(offset) - int(page_size), 1),
                                         int(page_size)))
    return meta
