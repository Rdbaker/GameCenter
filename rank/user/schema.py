# -*- coding: utf-8 -*-
"""User schemata."""
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from rank.user.models import User


class UserSchema(ModelSchema):
    """Schema for a User model."""
    class Meta:
        """Meta information for the UserSchema"""
        model = User

    id = fields.Int(required=True)
    username = fields.String(required=True)
    api_key = fields.Method('get_api_key')
    requests_today = fields.Method('get_request_count_today')
    frozen = fields.Method('get_is_frozen')

    def get_api_key(self, obj):
        return obj.game.api_key

    def get_request_count_today(self, obj):
        return obj.request_count_today()

    def get_is_frozen(self, obj):
        return obj.game.frozen
