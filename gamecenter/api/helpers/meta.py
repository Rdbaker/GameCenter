# -*- coding: utf-8 -*-
"""API helpers for META info."""
from flask import current_app


def get_meta_from_args(count, args):
    """Construct the meta dictionary from the args"""
    meta = {}
    uri = current_app.config['HOST_URI']
    meta['total'] = count
    meta['next'] = ((uri + "/api/leaderboards?offset={0}&page_size={1}")
                    .format(int(args['offset']) + int(args['page_size']), int(args['page_size'])))
    meta['prev'] = ((uri + "/api/leaderboards?offset={0}&page_size={1}")
                    .format(int(args['offset']) - int(args['page_size']), int(args['page_size'])))
    return meta
