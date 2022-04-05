"""Built-in functions for generating test responses.
"""
from __future__ import annotations

import math
import random
from datetime import datetime, timedelta
from string import digits, ascii_letters
from typing import TYPE_CHECKING, Any, Dict, Optional

import numpy as np
from sqlalchemy_mutable.utils import is_instance

from .base import Functional

if TYPE_CHECKING:
    from ..page import Page
    from ..questions.base import Question
    from ..questions.choice_base import ChoiceQuestion

CHARACTERS = digits + ascii_letters
TEXT_INPUT_TYPE = "text"
RANGE_INPUT_TYPE = "range"
NUMBER_INPUT_TYPE = "number"

test_response = Functional()

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


@test_response.register
def random_direction(page: "Page", pr_back: float = 0.2) -> str:
    """Chooses a random direction for navigation.

    Args:
        page (Page): Page to navigate from.
        pr_back (float, optional): Probability of going back if both forward and back
            navigation are available. This parameter is ignored if it is only possible
            to navigate in one direction. Defaults to 0.2.

    Raises:
        ValueError: If it is impossible to navigate from this page.

    Returns:
        str: "forward" or "back"
    """
    forward = bool(page.forward) and not page.is_last_page
    back = bool(page.back) and not page.is_first_page

    if not (forward or back):
        raise ValueError(f"Navigation is not possible from page {page}.")

    if forward and not back:
        return "forward"

    if back and not forward:
        return "back"

    return "back" if random.random() < pr_back else "forward"


@test_response.register
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

    if input_type in (NUMBER_INPUT_TYPE, RANGE_INPUT_TYPE):
        return random_number(input, **kwargs)

    if input_type in datetime_input_types:
        return random_datetime(input, **kwargs)

    return random_text(input, **kwargs)


@test_response.register
def random_text(question: "Question", pr_no_response: float = 0.2) -> Optional[str]:
    """Generate a random text response for an input-like question.

    Args:
        question (Question): Question, usually a :class:`hemlock.questions.input.Input`
            or :class:`hemlock.questions.textarea.Textarea`.
        pr_no_response (float, optional): Probability that the user doesn't respond.
            Defaults to .2.

    Returns:
        Optional[str]: Response.
    """
    # get the input or textarea HTML attributes
    tag: Dict[Any, Any] = {}
    if hasattr(question, "input_tag"):
        tag = question.input_tag
    elif hasattr(question, "textarea_tag"):
        tag = question.textarea_tag

    if not tag.get("required") and random.random() < pr_no_response:
        return None

    length = random.randint(tag.get("minlength", 1), tag.get("maxlength", 20))
    n_words = random.randint(tag.get("minwords", 1), tag.get("maxwords", 5))
    n_words = min(n_words, math.ceil(length / 2))
    n_whitespace_characters = n_words - 1
    word_length = int((length - n_whitespace_characters) / n_words)

    words = []
    for _ in range(n_words):
        words.append("".join(random.choices(CHARACTERS, k=word_length)))
    response = " ".join(words)

    if len(response) < length:
        # add additional characters if the response is too short
        response += "".join(random.choices(CHARACTERS, k=length - len(response)))
    return response


@test_response.register
def random_number(input: "Question", pr_no_response: float = 0.2) -> Optional[float]:
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
    if step == "any":
        step = random.choice((1., .1, .01))
    value = np.random.choice(np.arange(start, stop, step))
    if is_instance(start, int) and is_instance(stop, int) and is_instance(step, int):
        return int(value)
    # with a small step, you may encounter floating-point issues.
    # this rounds the response to the correct number of decimal places.
    # TODO: This isn't exactly correct. What about cases where min=1.01 and step=1?
    # Flagging for followup.
    return round(value, math.ceil(-math.log10(step)))


@test_response.register
def random_datetime(
    input: "Question", pr_no_response: float = 0.2
) -> Optional[datetime]:
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


@test_response.register
def random_choices(
    question: "ChoiceQuestion",
    pr_no_response: float = 0.2,
    min_choices: int = 0,
    max_choices: int = None,
) -> Any:
    """Select random choices as a test response.

    Args:
        question (ChoiceQuestion): Choice question.
        pr_no_response (float, optional): Probability that the user selects none of the
            choices. Defaults to 0.2.
        min_choices (int, optional): Minimum number of choices the user selects. Only
            relevant if the user can select multiple choices. Defaults to 0.
        max_choices (int, optional): Maximum number of choices the user selects. Only
            relevant if the user can select multiple choices. Defaults to None.

    Returns:
        Any: Choice value or set of choice values.
    """
    if random.random() < pr_no_response:
        return None

    choice_values = [
        choice["value"] for choice in question.choices if not choice.get("disabled")
    ]

    if question.multiple:
        if max_choices is None:
            max_choices = len(choice_values)

        n_choices = random.randint(min_choices, max_choices)
        return set(random.sample(choice_values, k=n_choices))

    return random.choice(choice_values)
