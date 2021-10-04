from itertools import combinations_with_replacement

import pytest

from hemlock.questions import Textarea

from . import utils


@pytest.mark.parametrize(
    "is_valid0, is_valid1", combinations_with_replacement((None, True, False), r=2)
)
def test_set_is_valid(is_valid0, is_valid1):
    utils.test_set_is_valid(is_valid0, is_valid1, Textarea, "textarea")
