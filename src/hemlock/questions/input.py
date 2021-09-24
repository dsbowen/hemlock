"""Input.
"""
from __future__ import annotations

import copy
from datetime import datetime
from typing import Mapping

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

    Subclasses :class:`hemlock.questions.base.Question`.

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
    def input_tag(self):
        return self.html_settings["input"]

    @property
    def response(self):
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

        Additionally adds appropriate validation classes to the input and feedback tags.
        """

        def add_and_remove_classes(html_attr, remove, add=None):
            classes = self.html_settings[html_attr]["class"]

            if not isinstance(remove, list):
                remove = [remove]
            for class_name in remove:
                try:
                    classes.remove(class_name)
                except ValueError:
                    pass

            if add is not None and add not in classes:
                classes.append(add)

        input_valid_class, input_invalid_class = "is-valid", "is-invalid"
        feedback_valid_class, feedback_invalid_class = (
            "valid-feedback",
            "invalid-feedback",
        )
        if is_valid is None:
            add_and_remove_classes(
                "input", remove=[input_valid_class, input_invalid_class]
            )
            add_and_remove_classes(
                "feedback", remove=[feedback_valid_class, feedback_invalid_class]
            )
        elif is_valid:
            add_and_remove_classes(
                "input", add=input_valid_class, remove=input_invalid_class
            )
            add_and_remove_classes(
                "feedback", add=feedback_valid_class, remove=feedback_invalid_class
            )
        else:
            add_and_remove_classes(
                "input", add=input_invalid_class, remove=input_valid_class
            )
            add_and_remove_classes(
                "feedback", add=feedback_invalid_class, remove=feedback_valid_class
            )

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
