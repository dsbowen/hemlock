from __future__ import annotations

import copy

from flask import render_template

from ..app import db
from ..utils.format import convert_markdown
from .base import Question


class Label(Question):
    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "label"}

    defaults = copy.deepcopy(Question.defaults)
    defaults["template"] = "hemlock/label.html"
    # form-label adds a margin after the text, which we don't want unless there's a
    # question below to respond to
    defaults["html_settings"]["label"]["class"].remove("form-label")

    def render(self):
        return render_template(
            self.template,
            question=self,
            label=None if self.label is None else convert_markdown(self.label, strip_last_paragraph=True)
        )
