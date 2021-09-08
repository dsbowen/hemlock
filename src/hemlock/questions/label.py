from __future__ import annotations

import copy

from ..app import db
from .base import Question


class Label(Question):
    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "label"}

    defaults = copy.deepcopy(Question.defaults)
    # form-label adds a margin after the text, which we don't want unless there's a
    # question below to respond to
    defaults["html_settings"]["label"]["class"].remove("form-label")
