"""Mixin for question objects with choice.
"""
from __future__ import annotations

import copy
import random
import textwrap
from typing import Any, Dict, List, Mapping, Tuple, Union

from flask import request
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_mutable.utils import is_instance

from .._custom_types import MutableChoiceListType
from ..app import db
from .base import Question

ChoiceType = Union[str, Tuple[Any, str], Mapping[Any, Any]]


def random_choices(
    question: ChoiceQuestion,
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
        Any: Choice value or list of choice values.
    """
    if random.random() < pr_no_response:
        return [] if question.multiple else None

    choice_values = [
        choice["value"] for choice in question.choices if not choice.get("disabled")
    ]

    if question.multiple:
        if max_choices is None:
            max_choices = len(choice_values)

        n_choices = random.randint(min_choices, max_choices)
        return random.sample(choice_values, k=n_choices)

    return random.choice(choice_values)


class ChoiceQuestion(Question):
    """Mixin for questions with choices.

    Subclasses :class:`Question`.

    Args:
        label (str, optional): Question label, prompt, or instructions. Defaults to
            None.
        choices (List[ChoiceType], optional): Choices that the user can select.
            Defaults to None.
        multiple (bool, optional): Indicates that the user can select multiple
            choices. Defaults to None.
        record_choice_indices (bool, optional): Indicates that the choice order should
        be recorded in the data frame. Defaults to None.
        **kwargs (Any): Additional keyword arguments passed to :class:`Question`
            constructor.

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

        return self.raw_response if self.multiple else self.raw_response[0]

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

    def is_default(self, choice: Dict[Any, Any]) -> bool:
        """Indicates that a given choice is a default.

        Args:
            choice (Dict[Any, Any]): Choice which may be a default.

        Returns:
            bool: Indicator that the choice is a default.

        Examples:

            .. doctest:

                >>> from hemlock.questions.choice_base import ChoiceQuestion
                >>> question = ChoiceQuestion(choices=["Yes", "No"], default="Yes")
                >>> question.is_default(question.choices[0])
                True
                >>> question.is_default(question.choices[1])
                False
        """
        default = self.get_default()

        if default is None:
            return False

        if is_instance(default, list):
            return choice["value"] in default

        return choice["value"] == default

    def record_response(self) -> None:
        """Record the user's raw response."""
        self.raw_response = [
            self.choices[int(i)]["value"] for i in request.form.getlist(self.hash)
        ]

    def record_data(self) -> None:
        """Record data based on the user's response."""
        if self.multiple:
            self.data = {
                choice["value"]: int(choice["value"] in self.raw_response)
                for choice in self.choices
            }
            return

        return super().record_data()

    def pack_data(self) -> "hemlock._data_frame.DataFrame":  # type: ignore
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
        """Create a raw rest response from a given test response.

        Args:
            response (Any): Test response. Must be either a choice value or list of
                choice values.

        Returns:
            List[Any]: List of indices of given choice values.
        """
        if response is None:
            return []

        if not isinstance(response, (list, tuple)):
            response = [response]

        choice_values = [choice["value"] for choice in self.choices]
        return [str(choice_values.index(value)) for value in response]
