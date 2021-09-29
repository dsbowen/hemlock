"""Check.
"""
from __future__ import annotations

import copy

from ..app import db
from .choice_base import ChoiceQuestion


class Check(ChoiceQuestion):
    """A check question allows users to select one or more choices by checking a box.

    Subclasses :class:`ChoiceQuestion`.
    """
    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "check"}

    defaults = copy.deepcopy(ChoiceQuestion.defaults)
    defaults["template"] = "hemlock/check.html"
