import re
from datetime import datetime
from decimal import Decimal
from itertools import product

import pytest

from hemlock import create_test_app
from hemlock.functional.test_response import (
    datetime_input_types,
    random_input,
    random_text,
    random_number,
    random_datetime,
    random_choices,
)
from hemlock.questions import Input, Textarea
from hemlock.questions.choice_base import ChoiceQuestion

INPUT_TYPES = ["text", "number", "range"] + list(datetime_input_types.keys())


@pytest.mark.parametrize("input_type, pr_no_response", product(INPUT_TYPES, (0, 1)))
def test_random_input(input_type, pr_no_response):
    expected_response_types = {key: datetime for key in datetime_input_types.keys()}
    expected_response_types.update(
        {"text": str, "number": (int, float), "range": (int, float)}
    )

    input = Input(input_tag={"type": input_type})
    response = random_input(input, pr_no_response=pr_no_response)
    if pr_no_response == 1:
        assert response is None
    else:
        assert isinstance(response, expected_response_types[input_type])


@pytest.mark.parametrize("question_cls", (Input, Textarea))
def test_random_text(question_cls):
    create_test_app()
    minlength, maxlength = 25, 60
    minwords, maxwords = 6, 10
    tag = {
        "minlength": minlength,
        "maxlength": maxlength,
        "minwords": minwords,
        "maxwords": maxwords,
    }
    if issubclass(question_cls, Input):
        question = Input(input_tag=tag)
    else:
        question = Textarea(textarea_tag=tag)
    response = random_text(question, pr_no_response=0)
    assert minlength <= len(response) <= maxlength
    assert minwords <= len(re.findall(r"\w+", response)) <= maxwords


def test_random_number():
    # test that random number can handle non-integer responses
    input = Input(input_tag={"type": "number", "step": 0.01})
    response = random_number(input, pr_no_response=0)
    # make sure the response has no more than 2 decimals
    assert -Decimal(str(response)).as_tuple().exponent <= 2


@pytest.mark.parametrize(
    "min_date, max_date", product((None, "1990-01-01"), (None, "2100-01-01"))
)
def test_random_datetime(min_date, max_date):
    # test than random datetime can handle min and max dates
    input = Input(input_tag={"type": "date", "min": min_date, "max": max_date})
    random_datetime(input, pr_no_response=0)


@pytest.mark.parametrize("multiple, pr_no_response", product((True, False), (0, 1)))
def test_random_choices(multiple, pr_no_response):
    choice_values = [0, 1, 2]
    question = ChoiceQuestion(
        choices=choice_values,
        multiple=multiple,
    )
    choices = random_choices(question, pr_no_response=pr_no_response)
    if pr_no_response == 1:
        assert choices is None
    else:
        if multiple:
            assert isinstance(choices, set)
            assert choices.issubset(choice_values)
        else:
            assert choices in choice_values
