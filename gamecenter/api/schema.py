# -*- coding: utf-8 -*-
"""API schemata."""
from marshmallow import fields
from marshmallow_sqlalchemy import ModelSchema

from gamecenter.api.models import Score


class ScoreSchema(ModelSchema):
    """Schema for a Score model."""
    class Meta:
        """Meta information for the ScoreSchema"""
        model = Score

    user_id = fields.Int(required=True)
    score = fields.Int(required=True)
