"""Textarea.
"""
from __future__ import annotations

import copy
from typing import Any, Mapping

import numpy as np
from flask import render_template
from sqlalchemy_mutable.html import HTMLAttrType

from ..app import db
from ..functional.test_response import random_text
from ..functional.validate import response_in_range
from .base import Question


class Textarea(Question):
    """Textarea.

    An textarea question allows users to enter a long free text response.

    Subclasses :class:`Question`.

    Args:
        *args (Any): Passed to :class:`Question` constructor.
        textarea_tag (Mapping[str, HTMLAttrType], optional): Additional attributes of
            the HTML textarea tag. Defaults to None.
        **kwargs (Any): Passed to :class:`Question` constructor.

    Attributes:
        textarea_tag (HTMLAttrsType): Attributes of the HTML textarea tag.
    """

    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "textarea"}

    defaults = copy.deepcopy(Question.defaults)
    defaults["template"] = "hemlock/textarea.html"  # type: ignore
    defaults["test_response"] = random_text
    defaults["html_settings"]["textarea"] = {
        "class": ["form-control w-100"],
        "style": {"height": "100px"},
    }

    @property
    def textarea_tag(self):
        return self.html_settings["textarea"]

    def __init__(
        self,
        *args: Any,
        textarea_tag: Mapping[str, HTMLAttrType] = None,
        **kwargs: Any,
    ):
        super().__init__(*args, **kwargs)
        self.html_settings["js"].append(
            render_template("hemlock/textarea.js", question=self)
        )
        if textarea_tag is not None:
            self.textarea_tag.update_attrs(textarea_tag)

    def set_is_valid(self, is_valid: bool = None) -> None:
        """See :meth:`Question.set_is_valid`.

        Additionally adds appropriate validation classes to the textarea tag.
        """
        return_value = super().set_is_valid(is_valid)
        self._add_or_remove_class("textarea", "is-valid", is_valid is True)
        self._add_or_remove_class("textarea", "is-invalid", is_valid is False)
        return return_value

    def run_validate_functions(self) -> bool:
        """See :meth:`Question.run_validate_functions`.

        Additionally, this method validates that the user's response has the correct
        word count.
        """
        if self.response is not None:
            minwords = self.textarea_tag.get("minwords")
            if minwords is None:
                minwords = 0

            maxwords = self.textarea_tag.get("maxwords")
            if maxwords is None:
                maxwords = np.inf

            if (
                response_in_range(self, minwords, maxwords, how="word count")
                is not None
            ):
                if minwords == 0:
                    self.feedback = f"Please shorten your response to {maxwords} words."
                elif maxwords == np.inf:
                    self.feedback = f"Please write at least {minwords} words."
                else:
                    # both minwords and maxwords are defined
                    self.feedback = (
                        f"Please write between {minwords} and {maxwords} words."
                    )

                self.set_is_valid(False)
                return False

        return super().run_validate_functions()
