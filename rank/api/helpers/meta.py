# -*- coding: utf-8 -*-
"""API helpers for META info."""
import urllib

from flask import current_app


def get_meta_from_args(count, args, endpoint):
    """Construct the meta dictionary from the args"""
    meta = {}
    uri = current_app.config['HOST_URI']
    offset = args['offset']
    page_size = args['page_size']
    meta['total'] = count
    meta['links'] = {}

    ret_args = {}
    if endpoint == "leaderboards":
        for p in ('user_id', 'sort', 'tag', 'start_date', 'end_date'):
            if args[p]:
                ret_args[p] = args[p]
    elif endpoint == "add_score_and_list":
        for p in ('sort', 'tag', 'start_date', 'end_date'):
            if args[p]:
                ret_args[p] = args[p]

    if offset + page_size < count:
        ret_args.update({"offset": min(int(offset) + int(page_size), count), "page_size": int(page_size)})
        meta['links']['next'] = (uri + "/api/leaderboards?" + urllib.urlencode(ret_args))
    if offset > 1:
        ret_args.update({"offset": max(int(offset) - int(page_size), 1), "page_size": int(page_size)})
        meta['links']['prev'] = (uri + "/api/leaderboards?" + urllib.urlencode(ret_args))
    return meta
