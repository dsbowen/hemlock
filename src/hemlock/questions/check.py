from __future__ import annotations

import copy

from ..app import db
from .base import ChoiceQuestion


class Check(ChoiceQuestion):
    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "check"}

    defaults = copy.deepcopy(ChoiceQuestion.defaults)
    defaults["template"] = "hemlock/check.html"
