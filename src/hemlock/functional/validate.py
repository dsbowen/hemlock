"""Built-in validate functions.
"""
from __future__ import annotations

import operator
import re
from decimal import Decimal
from typing import TYPE_CHECKING, Any, Callable, Iterable, Optional, Tuple, Union

from sqlalchemy_mutable.utils import get_object, is_instance

from .base import Functional

if TYPE_CHECKING:
    from ..questions.base import Question

HOW_TO_TRANSFORM = {
    "value": lambda question: question.response,
    "length": lambda question: len(question.response),
    "word count": lambda question: len(
        re.findall("\w+", get_object(question.response))
    ),
    "decimals": lambda question: -Decimal(get_object(question.raw_response))
    .as_tuple()
    .exponent,
}

ComparisonType = Union[str, Callable[[Any, Any], bool]]
FeedbackType = Optional[Union[bool, Tuple[bool, Optional[str]]]]
HowType = Union[str, Callable[["Question"], Any]]

validate = Functional()


@validate.register
def require_response(question: "Question", feedback: str = None) -> FeedbackType:
    """Require a response.

    Args:
        question (Question): Question.
        feedback (str, optional): Feedback if the user didn't respond. Defaults to None.

    Returns:
        FeedbackType: Feedback.
    """
    if question.response in (None, set()):
        return False, feedback
    return None


@validate.register
def response_in(
    question: "Question", valid_set: Iterable, feedback: str = None
) -> FeedbackType:
    """Require that the user's response be in a given set.

    Args:
        question (Question): Question.
        valid_set (Iterable): Set of valid responses.
        feedback (str, optional): Feedback if the user's response isn't in the valid
            set. Defaults to None.

    Returns:
        FeedbackType: Feedback.
    """
    if question.response not in valid_set:
        return False, feedback
    return None


@validate.register
def response_not_in(
    question: "Question", invalid_set: Iterable, feedback: str = None
) -> FeedbackType:
    """Require that the user's response not be in a given set.

    Args:
        question (Question): Question.
        invalid_set (Iterable): Set of invalid responses.
        feedback (str, optional): Feedback if the user's response is in the invalid
            set. Defaults to None.

    Returns:
        FeedbackType: Feedback.
    """
    if question.response in invalid_set:
        return False, feedback
    return None


@validate.register
def compare_response(
    question: "Question",
    value: Any,
    feedback: str = None,
    comparison: ComparisonType = "==",
    how: HowType = "value",
) -> FeedbackType:
    """Require that the user's response satsify a comparison.

    Args:
        question (Question): Question.
        value (Any): Value to which the response will be compared.
        feedback (str, optional): Feedback if the comparison fails. Defaults to None.
        comparison (ComparisonType, optional): Comparison operator. Defaults to ==.
        how (HowType, optional): How the response should be assessed ("value",
            "length", "word count", or "decimals"). Defaults to value.

    Returns:
        FeedbackType: Feedback.
    """
    from ..questions.base import Question

    string_to_operator = {
        "<": operator.lt,
        "<=": operator.le,
        "==": operator.eq,
        "!=": operator.ne,
        ">=": operator.ge,
        ">": operator.gt,
    }
    transform_response = HOW_TO_TRANSFORM[how] if is_instance(how, str) else how  # type: ignore

    response = transform_response(question)  # type: ignore

    if is_instance(value, Question):
        value = transform_response(value)  # type: ignore

    if is_instance(comparison, str):
        comparison = string_to_operator[comparison]  # type: ignore

    if not comparison(response, value):  # type: ignore
        return False, feedback
    return None


@validate.register
def response_in_range(
    question: "Question",
    min_value: Any,
    max_value: Any,
    feedback: str = None,
    how: HowType = "value",
) -> FeedbackType:
    """Require the user's response to be in a given range of values.

    Args:
        question (Question): Question.
        min_value (Any): Minimum value.
        max_value (Any): Maximum value.
        feedback (str, optional): Feedback if the response is not in the required
            range. Defaults to None.
        how (HowType, optional): How the response should be assessed ("value",
            "length", "word count", or "decimals"). Defaults to value.

    Returns:
        FeedbackType: Feedback.
    """
    response = HOW_TO_TRANSFORM[how](question)  # type: ignore
    if not (min_value <= response <= max_value):
        return False, feedback
    return None


@validate.register
def re_full_match(
    question: "Question",
    pattern: str,
    feedback: str = None,
    flags: Any = 0,
) -> FeedbackType:
    """Require that the user's response match a regular expression.

    Args:
        question (Question): Question.
        pattern (str): Regular expression pattern.
        feedback (str, optional): Feedback if the response does not match the pattern.
            Defaults to None.
        flags (Any, optional): Flags (see python documentation on ``re.fullmatch``).
            Defaults to 0.

    Returns:
        FeedbackType: Feedback.
    """
    if not re.fullmatch(pattern, question.response, flags):
        return False, feedback
    return None
