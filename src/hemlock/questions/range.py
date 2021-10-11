"""Range.
"""
from __future__ import annotations

import copy
from typing import Any, Mapping, Optional

from flask import render_template
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_mutable.html import HTMLAttrType
from sqlalchemy_mutable.utils import partial

from ..app import db
from ..functional.test_response import random_number
from .base import Question


class Range(Question):
    """Range.

    An range question allows users to enter a numeric response using a range slider.

    Subclasses :class:`hemlock.questions.base.Question`.

    Args:
        *args (Any): Passed to :class:`hemlock.questions.base.Question` constructor.
        input_tag (Mapping[str, HTMLAttrType], optional): Additional attributes of the
            HTML input tag. Defaults to None.
        **kwargs (Any): Passed to :class:`hemlock.questions.base.Question` constructor.
    """

    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "range"}

    defaults = copy.deepcopy(Question.defaults)
    defaults["template"] = "hemlock/range.html"  # type: ignore
    defaults["html_settings"]["input"] = {"type": "range", "class": ["form-range"]}  # type: ignore
    defaults["test_response"] = partial(random_number, pr_no_response=0)

    @property
    def input_tag(self) -> HTMLAttrType:
        """Attributes of the HTML input tag.

        Returns:
            HTMLAttrType: HTML attributes.
        """
        return self.html_settings["input"]

    @hybrid_property
    def response(self) -> Optional[float]:
        """See :meth:`hemlock.questions.base.Question.response`."""
        return None if self.raw_response is None else float(self.raw_response)

    def __init__(
        self, *args: Any, input_tag: Mapping[str, HTMLAttrType] = None, **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        self.html_settings["js"].append(
            render_template("hemlock/range.js", question=self)
        )
        if input_tag is not None:
            self.input_tag.update_attrs(input_tag)

    def make_raw_test_response(self, response: float) -> str:
        """See :meth:`hemlock.questions.base.Question.make_raw_test_response`."""
        return str(response)
