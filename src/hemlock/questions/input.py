"""Input.
"""
from __future__ import annotations

import copy
from datetime import datetime

from typing import Any, Mapping

from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_mutable.html import HTMLAttrType
from sqlalchemy_mutable.utils import is_instance

from ..app import db
from ..functional.test_response import datetime_input_types, random_input
from .base import Question

TEXT_INPUT_TYPE = "text"
NUMBER_INPUT_TYPE = "number"


class Input(Question):
    """Input.

    An input question allows users to enter a free text response.

    Subclasses :class:`hemlock.questions.base.Question`.

    Args:
        *args (Any): Passed to :class:`hemlock.questions.base.Question` constructor.
        input_tag (Mapping[str, HTMLAttrType], optional): Additional attributes of the
            HTML input tag. Defaults to None.
        **kwargs (Any): Passed to :class:`hemlock.questions.base.Question` constructor.

    Examples:
        The most common use of the ``input_tag`` attribute is for setting the input
        type. For example, let's require users to enter a number.

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

        You can also require users to enter a certain input length.

        .. doctest::

            >>> from hemlock.questions import Input
            >>> question = Input(input_tag={"minlength": 5, "maxlength": 10})
            >>> question.input_tag["minlength"], question.input_tag["maxlength"]
            (5, 10)
    """

    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "input"}

    defaults = copy.deepcopy(Question.defaults)
    defaults["template"] = "hemlock/input.html"  # type: ignore
    defaults["html_settings"]["input"] = {"type": TEXT_INPUT_TYPE, "class": ["form-control"]}  # type: ignore
    defaults["test_response"] = random_input

    @property
    def input_tag(self) -> HTMLAttrType:
        """Attributes of the HTML input tag.

        Returns:
            HTMLAttrType: HTML attributes.
        """
        return self.html_settings["input"]

    @hybrid_property
    def response(self) -> Any:
        """Converts the raw response to the appropriate type based on the input type."""
        if self.raw_response in ("", None):
            return None

        input_type = self.input_tag.get("type", TEXT_INPUT_TYPE)

        if input_type == NUMBER_INPUT_TYPE:
            return float(self.raw_response)

        if input_type in datetime_input_types:
            _, datetime_format = datetime_input_types[input_type]
            return datetime.strptime(self.raw_response.get_object(), datetime_format)

        return str(self.raw_response)

    def __init__(
        self, *args: Any, input_tag: Mapping[str, HTMLAttrType] = None, **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        if input_tag is not None:
            self.input_tag.update_attrs(input_tag)

    def set_is_valid(self, is_valid: bool = None) -> None:
        """See :meth:`hemlock.questions.base.Question.set_is_valid`.

        Additionally adds appropriate validation classes to the input tag.
        """
        return_value = super().set_is_valid(is_valid)
        self._add_or_remove_class("input", "is-valid", is_valid is True)
        self._add_or_remove_class("input", "is-invalid", is_valid is False)
        return return_value

    def run_validate_functions(self) -> bool:
        """See :meth:`hemlock.questions.base.Question.run_validate_functions`.

        Additionally, this method validates that the user's response matches the input
        type.
        """
        input_type = self.input_tag.get("type", TEXT_INPUT_TYPE)

        # tests if the raw response can be converted to the expected type
        try:
            self.response
        except ValueError:
            if input_type == NUMBER_INPUT_TYPE:
                self.feedback = "Please enter a number."
            elif input_type in datetime_input_types:
                html_format, datetime_format = datetime_input_types[input_type]
                self.feedback = f"Please use the format {html_format}. For example, right now it is {datetime.utcnow().strftime(datetime_format)}."
            else:
                self.feedback = "Please enter the correct type of response."

            self.set_is_valid(False)
            return False

        return super().run_validate_functions()

    def make_raw_test_response(self, response: Any) -> str:
        """Make a raw test response from the given response.

        Args:
            response (Any): Given response.

        Raises:
            ValueError: If the input is a number, the response must be convertible to
                float.
            ValueError: If the input is a date or time, the response must be in the
                correct datetime format.

        Returns:
            str: Raw response
        """
        if response is None:
            return ""

        input_type = self.input_tag.get("type", TEXT_INPUT_TYPE)

        # make sure the raw response is in the expected format
        if input_type == NUMBER_INPUT_TYPE:
            try:
                float_response = float(response)
            except ValueError:
                raise ValueError(
                    f"Response {repr(response)} to input {self} cannot be converted to a float."
                )
            # make sure raw response is in the correct value range
            if (
                min_value := self.input_tag.get("min")
            ) is not None and float_response < float(min_value):
                raise ValueError(f"Reponse {response} is less than min {min_value}.")
            if (
                max_value := self.input_tag.get("max")
            ) is not None and float_response > float(max_value):
                raise ValueError(f"Response {response} is greater than max {max_value}")
            return str(response)

        if input_type in datetime_input_types:
            # raw response can either be a string in HTML format or a datetime object
            html_format, datetime_format = datetime_input_types[input_type]
            if isinstance(response, datetime):
                return response.strftime(datetime_format)

            try:
                datetime.strptime(response, datetime_format)
            except ValueError:
                raise ValueError(
                    f"Response {repr(response)} to input {self}"
                    f" does not match format {html_format}."
                    " For example, right now it is"
                    f" {datetime.utcnow().strftime(datetime_format)}."
                )
            return response

        if input_type == TEXT_INPUT_TYPE and not is_instance(response, str):
            raise ValueError(
                f"Error on input {self}"
                f"\nThis input accepts any text but the test response was {response} of"
                f" type {type(response)}. A common cause of this error is that you want"
                " users to enter a number but didn't require the input type to be a"
                " number. You can do this with:"
                '\n>>> Input(input_tag={"type": "number"})'
            )

        return str(response)
