"""Input.
"""
from __future__ import annotations

import copy
from datetime import datetime
from typing import Any, Mapping

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_mutable.html import HTMLAttrType

from ..app import db
from .base import Question


# map input types to (HTML format, datetime format)
# where HTML format is the raw format from the post request
# and datetime format is the format expected by python's datetime module
datetime_input_types = {
    "date": ("yyyy-mm-dd", "%Y-%m-%d"),
    "datetime": ("yyyy-mm-ddTHH:MM", "%Y-%m-%dT%H:%M"),
    "datetime-local": ("yyyy-mm-ddTHH:MM", "%Y-%m-%dT%H:%M"),
    "month": ("yyyy-mm", "%Y-%m"),
    "time": ("HH:MM", "%H:%M"),
}


class Input(Question):
    """An input question allows user to enter a free text response.

    Subclasses :class:`Question`.

    Args:
        input_tag (Mapping[str, HTMLAttrType], optional): Additional attributes of the
            HTML input tag. Defaults to None.

    Attributes:
        input_tag (HTMLAttrsType): Attributes of the HTML input tag.

    Examples:
        The most common use of the `input_tag` attribute is for setting the input type.
        For example, let's require users to enter a number.

        .. doctest::

            >>> from hemlock.questions import Input
            >>> question = Input(input_tag={"type": "number"})
            >>> question.input_tag["type"]
            'number'

        Let's require users to enter a number between 0 and 10.

        .. doctest::

            >>> from hemlock.questions import Input
            >>> question = Input(input_tag={"type": "number", "min": 0, "max": 10})
            >>> question.input_tag["min"], question.input_tag["max"]
            (0, 10)
    """

    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "input"}

    defaults = copy.deepcopy(Question.defaults)
    defaults["template"] = "hemlock/input.html"  # type: ignore
    defaults["html_settings"]["input"] = {"type": "text", "class": ["form-control"]}  # type: ignore

    @property
    def input_tag(self) -> HTMLAttrType:
        return self.html_settings["input"]

    @hybrid_property
    def response(self) -> Any:
        """Converts the raw response to the appropriate type based on the input type."""
        if self.raw_response in ("", None):
            return None

        input_type = self.input_tag.get("type", "text")

        if input_type == "number":
            return float(self.raw_response)

        if input_type in datetime_input_types:
            _, datetime_format = datetime_input_types[input_type]
            return datetime.strptime(self.raw_response.get_object(), datetime_format)

        return str(self.raw_response)

    def __init__(self, *args, input_tag: Mapping[str, HTMLAttrType] = None, **kwargs):
        super().__init__(*args, **kwargs)
        if input_tag is not None:
            self.input_tag.update_attrs(input_tag)

    def set_is_valid(self, is_valid: bool = None):
        """See :meth:`hemlock.questions.base.Question.set_is_valid`.

        Additionally adds appropriate validation classes to the input tag.
        """
        valid_class, invalid_class = "is-valid", "is-invalid"
        if is_valid is None:
            self._add_and_remove_classes("input", remove=[valid_class, invalid_class])
        elif is_valid:
            self._add_and_remove_classes("input", add=valid_class, remove=invalid_class)
        else:
            self._add_and_remove_classes("input", add=invalid_class, remove=valid_class)

        return super().set_is_valid(is_valid)

    def run_validate_functions(self) -> bool:
        """See :meth:`hemlock.questions.base.Question.run_validate_functions`.

        Additionally validates that the user's response matches the input type.
        """
        try:
            # tests if the raw response can be converted to the expected type
            self.response
        except ValueError:
            input_type = self.input_tag.get("type", "text")
            if input_type == "number":
                self.feedback = "Please enter a number."
            elif input_type in datetime_input_types:
                html_format, datetime_format = datetime_input_types[input_type]
                self.feedback = f"Please use the format {html_format}. For example, right now it is {datetime.utcnow().strftime(datetime_format)}."
            else:
                self.feedback = "Please enter the correct type of response."

            self.set_is_valid(False)
            return False

        return super().run_validate_functions()
