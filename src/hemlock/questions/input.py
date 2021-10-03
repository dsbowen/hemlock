"""Input.
"""
from __future__ import annotations

import copy
import math
import random
from datetime import datetime, timedelta
from string import digits, ascii_letters
from typing import Any, Mapping

import numpy as np
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_mutable.html import HTMLAttrType
from sqlalchemy_mutable.utils import is_instance

from ..app import db
from .base import Question

CHARACTERS = digits + ascii_letters
TEXT_INPUT_TYPE = "text"
NUMBER_INPUT_TYPE = "number"


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

from typing import Optional


def random_input(input: Question, **kwargs: Any) -> Any:
    """Generate a random response for an input-like question.

    Args:
        input (Question): Input question.
        **kwargs (Any): Passed to :func:`random_text`, :func:`random_number`, or
            :func:`random_datetime`, depending on the input type.

    Returns:
        Any: Response.
    """
    input_type = input.input_tag.get("type", TEXT_INPUT_TYPE)

    if input_type == NUMBER_INPUT_TYPE:
        return random_number(input, **kwargs)

    if input_type in datetime_input_types:
        return random_datetime(input, **kwargs)

    return random_text(input, **kwargs)


def random_text(
    input: Question, pr_no_response: float = 0.2, min_words: int = 1, max_words: int = 5
) -> Optional[str]:
    """Generate a random text response for an input-like question.

    Args:
        input (Question): Input question.
        pr_no_response (float, optional): Probability that the user doesn't respond.
            Defaults to .2.
        min_words (int, optional): Minimum number of words. Defaults to 1.
        max_words (int, optional): Maximum number of words. Defaults to 5.

    Returns:
        Optional[str]: Response.
    """
    if not input.input_tag.get("required") and random.random() < pr_no_response:
        return None

    length = random.randint(
        input.input_tag.get("minlength", 1), input.input_tag.get("maxlength", 20)
    )
    n_words = random.randint(min_words, max_words)
    n_words = min(n_words, math.ceil(length / 2))
    n_whitespace_characters = n_words - 1
    word_length = int((length - n_whitespace_characters) / n_words)

    words = []
    for _ in range(n_words):
        words.append("".join(random.choices(CHARACTERS, k=word_length)))
    response = " ".join(words)

    if len(response) < length:
        # add additional characters if the response is too short
        response += "".join(random.choices(CHARACTERS, k=len(response) - length))
    return response


def random_number(input: Question, pr_no_response: float = 0.2) -> Optional[float]:
    """Generate a random number response for an input-like question.

    Args:
        input (Question): Input question.
        pr_no_response (float, optional): Probability that the user doesn't respond.
            Defaults to .2.

    Returns:
        Optional[float]: Response.
    """
    if not input.input_tag.get("required") and random.random() < pr_no_response:
        return None

    input_tag = input.input_tag
    start = input_tag.get("min", -10000)
    stop = input_tag.get("max", 10000)
    step = input_tag.get("step", 1)
    value = np.random.choice(np.arange(start, stop, step))
    if is_instance(start, int) and is_instance(stop, int) and is_instance(step, int):
        return int(value)
    # with a small step, you may encounter floating-point issues.
    # this rounds the response to the correct number of decimal places.
    return round(value, math.ceil(-math.log10(step)))


def random_datetime(input: Question, pr_no_response: float = 0.2) -> Optional[datetime]:
    """Generate a random datetime response for an input-like question.

    Args:
        input (Question): Input question.
        pr_no_response (float, optional): Probability that the user doesn't respond.
            Defaults to .2.

    Returns:
        Optional[datetime]: Response.
    """
    if not input.input_tag.get("required") and random.random() < pr_no_response:
        return None

    def get_datetime(key):
        raw_value = input_tag.get(key)
        if raw_value is None:
            delta = timedelta(weeks=100 * 52)  # 100 years
            if key == "min":
                return datetime.utcnow() - delta
            return datetime.utcnow() + delta
        return datetime.strptime(raw_value, datetime_format)

    input_tag = input.input_tag
    input_type = input_tag["type"]
    _, datetime_format = datetime_input_types[input_type]
    start, stop = get_datetime("min"), get_datetime("max")
    return start + timedelta(seconds=np.random.uniform((stop - start).total_seconds()))


class Input(Question):
    """Input.
    
    An input question allows users to enter a free text response.

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
    defaults["html_settings"]["input"] = {"type": TEXT_INPUT_TYPE, "class": ["form-control"]}  # type: ignore
    defaults["test_response"] = random_input

    @property
    def input_tag(self) -> HTMLAttrType:
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

    def __init__(self, *args, input_tag: Mapping[str, HTMLAttrType] = None, **kwargs):
        super().__init__(*args, **kwargs)
        if input_tag is not None:
            self.input_tag.update_attrs(input_tag)

    def set_is_valid(self, is_valid: bool = None):
        """See :meth:`hemlock.questions.base.Question.set_is_valid`.

        Additionally adds appropriate validation classes to the input tag.
        """
        return_value = super().set_is_valid(is_valid)
        self._set_validation_classes("input", "is-valid", "is-invalid")
        return return_value

    def run_validate_functions(self) -> bool:
        """See :meth:`hemlock.questions.base.Question.run_validate_functions`.

        Additionally validates that the user's response matches the input type.
        """
        try:
            # tests if the raw response can be converted to the expected type
            self.response
        except ValueError:
            input_type = self.input_tag.get("type", TEXT_INPUT_TYPE)
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
                float(response)
            except ValueError:
                raise ValueError(
                    f"Response {repr(response)} to input {self} cannot be converted to a float."
                )
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
                    f"Response {repr(response)} to input {self} does not match format {html_format}. For example, right now it is {datetime.utcnow().strftime(datetime_format)}."
                )
            return response

        return str(response)
