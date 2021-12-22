from itertools import combinations_with_replacement, product

import numpy as np
import pytest

from hemlock import User, Page
from hemlock.questions import Textarea

from . import utils
from ..utils import app


@pytest.mark.parametrize(
    "is_valid0, is_valid1", combinations_with_replacement((None, True, False), r=2)
)
def test_set_is_valid(app, is_valid0, is_valid1):
    utils.test_set_is_valid(is_valid0, is_valid1, Textarea, "textarea")


@pytest.mark.parametrize(
    "minwords, maxwords, response",
    product(
        (None, 2),
        (None, 2),
        (None, "one", "two words", "three different words"),
    ),
)
def test_word_count(app, minwords, maxwords, response):
    def seed():
        return [
            Page(Textarea(textarea_tag={"minwords": minwords, "maxwords": maxwords})),
            Page(),
        ]

    user = User.make_test_user(seed)
    user.test_request([response])
    question = user.get_tree().branch[0].questions[0]

    minwords = minwords or 0
    maxwords = maxwords or np.inf
    if response is None or minwords <= len(response.split(" ")) <= maxwords:
        assert question.is_valid is None
    else:
        assert question.is_valid is False
