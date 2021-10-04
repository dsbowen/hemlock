"""Select.
"""
from __future__ import annotations

import copy

from sqlalchemy_mutable.html import HTMLAttrType

from ..app import db
from .choice_base import ChoiceQuestion


class Select(ChoiceQuestion):
    """Select.

    A select question allows users to select one or more choices using a dropdown menu.

    Subclasses :class:`ChoiceQuestion`.

    Attributes:
        select_tag (HTMLAttrsType): Attributes of the HTML select tag.
    """

    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "select"}

    defaults = copy.deepcopy(ChoiceQuestion.defaults)
    defaults["template"] = "hemlock/select.html"
    defaults["html_settings"]["select"] = {"class": ["form-select"]}

    @property
    def select_tag(self) -> HTMLAttrType:
        return self.html_settings["select"]

    def set_is_valid(self, is_valid: bool = None) -> None:
        """See :meth:`hemlock.questions.base.Question.set_is_valid`.

        Additionally adds appropriate validation classes to the select tag.
        """
        return_value = super().set_is_valid(is_valid)
        self._add_or_remove_class("select", "is-valid", is_valid is True)
        self._add_or_remove_class("select", "is-invalid", is_valid is False)
        return return_value
