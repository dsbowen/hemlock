from datetime import date
import random

import pytest

from hemlock import User, Page, create_test_app
from hemlock.questions import Check, Input, Label, Range, Select, Textarea
from hemlock.questions.input import datetime_input_types

SKIP = True

random.seed(123)


def seed():
    return [
        Page(Check(choices=list(range(3))), back=True),
        Page(Check(choices=list(range(3)), multiple=True), back=True),
        *[
            Page(Input(input_tag={"type": input_type}), back=True)
            for input_type in datetime_input_types.keys()
        ],
        Page(Range(), back=True),
        Page(Select(choices=list(range(3))), back=True),
        Page(Select(choices=list(range(3)), multiple=True), back=True),
        Page(Textarea(), back=True),
        Page(Label("The end!"), back=True),
    ]


@pytest.mark.skipif(SKIP, reason="Long-running test.")
def test():
    create_test_app()
    User.test_multiple_users(20, seed)
