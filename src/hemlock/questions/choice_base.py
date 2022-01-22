"""Mixin for question objects with choice.
"""
from __future__ import annotations

import copy
import textwrap
from typing import TYPE_CHECKING, Any, Dict, List, Mapping, Tuple, Union

from flask import request
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_mutable.utils import is_instance

from .._custom_types import MutableChoiceListType
from ..app import db
from ..functional.test_response import random_choices
from .base import Question

if TYPE_CHECKING:
    from .._data_frame import DataFrame

ChoiceType = Union[str, Tuple[Any, str], Mapping[Any, Any]]


class ChoiceQuestion(Question):
    """Mixin for questions with choices.

    Subclasses :class:`hemlock.questions.base.Question`.

    Args:
        label (str, optional): Question label, prompt, or instructions. Defaults to
            None.
        choices (List[ChoiceType], optional): Choices that the user can select.
            Defaults to None.
        multiple (bool, optional): Indicates that the user can select multiple
            choices. Defaults to None.
        record_choice_indices (bool, optional): Indicates that the choice order should
        be recorded in the data frame. Defaults to None.
        **kwargs (Any): Additional keyword arguments passed to the
            :class:`hemlock.questions.base.Question` constructor.

    Attributes:
        choices (List[Dict[Any, Any]]): Choices that the user can select.
        multiple (bool): Indicates that the user can select multiple choices.
        record_choice_indices (bool): Indicates that the choice order should be recorded
            in the data frame.

    """

    defaults = copy.deepcopy(Question.defaults)
    defaults.update(
        {
            "choices": [],
            "multiple": False,
            "test_response": random_choices,
            "record_choice_indices": False,
        }
    )

    choices = db.Column(MutableChoiceListType)
    choice_template = db.Column(db.String)
    multiple = db.Column(db.Boolean)
    record_choice_indices = db.Column(db.Boolean)

    @hybrid_property
    def response(self) -> Any:
        """Returns the user's response based on the user's raw response.

        Returns:
            Any: User's response.
        """
        if not self.raw_response and not self.multiple:
            return None

        return self.raw_response if self.multiple else next(iter(self.raw_response))

    def __init__(
        self,
        label: str = None,
        choices: List[ChoiceType] = None,
        multiple: bool = None,
        record_choice_indices: bool = None,
        **kwargs: Any,
    ):
        super().__init__(label, **kwargs)
        self._set_default_attribute("choices", choices, True)
        self._set_default_attribute("multiple", multiple)
        self._set_default_attribute("record_choice_indices", record_choice_indices)

    def __repr__(self):
        initial_indent = ""
        subsequent_indent = 4 * " "
        max_choices = 4
        placeholder = "[...]"
        question_text = super().__repr__()

        if not self.choices:
            choice_text = ""
        else:
            choice_values = [
                f"- {choice['value']}" for choice in self.choices[:max_choices]
            ]
            if len(choice_values) == max_choices:
                choice_values.append(placeholder)
            choice_text = "\n".join(choice_values)
            choice_text = f"\n{textwrap.indent(choice_text, subsequent_indent)}"

        return textwrap.indent(question_text + choice_text, initial_indent)

    def is_default(self, value: Any) -> bool:
        """Indicates that a given choice value is a default.

        Args:
            value (Any): Value to check.

        Returns:
            bool: Indicator that the choice value is a default.

        Examples:

            .. doctest::

                >>> from hemlock.questions.choice_base import ChoiceQuestion
                >>> question = ChoiceQuestion(choices=["Yes", "No"], default="Yes")
                >>> question.is_default("Yes")
                True
                >>> question.is_default("No")
                False

            Use a ``list`` to indicate that there are multiple default values.

            .. doctest::

                >>> from hemlock.questions.choice_base import ChoiceQuestion
                >>> question = ChoiceQuestion(choices=["Red", "Green", "Blue"], multiple=True, default=["Red", "Green"])
                >>> question.is_default("Red")
                True
                >>> question.is_default("Green")
                True
                >>> question.is_default("Blue")
                False
        """
        default = self.get_default()

        if default is None:
            return False

        if is_instance(default, (list, set)):
            return value in default

        return value == default

    def record_response(self) -> None:
        """Record the user's raw response.

        The raw response is a set of choice values.
        """
        # Note: jinja template loop indices start at 1, so we need to subtract 1 for 0 indexing
        self.raw_response = {
            self.choices[int(i) - 1]["value"] for i in request.form.getlist(self.hash)
        }

    def record_data(self) -> None:
        """Record data based on the user's response."""
        if self.multiple:
            self.data = {
                choice["value"]: int(choice["value"] in self.raw_response)
                for choice in self.choices
            }
            return

        return super().record_data()

    def pack_data(self) -> DataFrame:
        """Pack the data for insertion into a data frame."""
        dataframe = super().pack_data()
        if self.variable is None or not self.record_choice_indices:
            return dataframe

        choice_indices = {}
        for i, choice in enumerate(self.choices):
            choice_indices[f"{self.variable}_{choice['value']}_index"] = i
        dataframe.add_data(choice_indices, fill_rows=True)
        dataframe.pad()
        return dataframe

    def make_raw_test_response(self, response: Any) -> List[Any]:
        """Create a raw test response from a given test response.

        Args:
            response (Any): Test response. Must be either a choice value or a set of
                choice values.

        Returns:
            List[Any]: List of indices of given choice values.
        """
        if response is None:
            return []

        if not is_instance(response, (list, set)):
            response = {response}

        # check that test responses are valid choices
        if invalid_responses := set(response) - set(
            choice["value"] for choice in self.choices
        ):
            raise ValueError(
                f"Test user chose invalid choices {invalid_responses} for\n{self}."
            )

        # Note: jinja template loop indices start at 1, so we need to add 1 for 1 indexing
        return [
            str(i + 1)
            for i, choice in enumerate(self.choices)
            if choice["value"] in response
        ]
