"""Built-in compile functions.
"""
from __future__ import annotations

from typing import TYPE_CHECKING, Union

from .base import Functional

if TYPE_CHECKING:  # pragma: no cover
    from ..page import Page
    from ..questions.base import Question

compile = Functional()


@compile.register
def clear_feedback(obj: Union["Page", "Question"]) -> None:
    """Clear feedback.

    Args:
        obj (Union[Page, Question]): Page or question whose feedback will be cleared.
    """
    obj.clear_feedback()


@compile.register
def clear_response(obj: Union["Page", "Question"]) -> None:
    """Clear response.

    Args:
        obj (Union[Page, Question]): Page or question whose responses will be cleared.
    """
    obj.clear_response()
