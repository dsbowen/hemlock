import operator
import re
from decimal import Decimal
from itertools import product

import pytest

from hemlock import User, Page, create_test_app
from hemlock.functional import validate
from hemlock.questions import Check, Input


def make_test_question(seed, response):
    create_test_app()
    user = User.make_test_user(seed)
    user.test_request([response])
    return user.get_tree().branch[0].questions[0]


@pytest.mark.parametrize(
    "choice_question, response",
    ((True, None), (True, 0), (True, {0, 1}), (False, None), (False, "test response")),
)
def test_require_response(choice_question, response):
    def seed():
        question = (
            Check(choices=[0, 1, 2], multiple=True) if choice_question else Input()
        )
        question.validate = validate.require_response()
        return [Page(question), Page()]

    question = make_test_question(seed, response)
    if response is None:
        assert question.is_valid is False
    else:
        assert question.is_valid is not False


@pytest.mark.parametrize("response", ("a", "b"))
def test_response_in(response):
    valid_set = ("b", "c")

    def seed():
        return [Page(Input(validate=validate.response_in(valid_set))), Page()]

    question = make_test_question(seed, response)
    if response in valid_set:
        assert question.is_valid is not False
    else:
        assert question.is_valid is False


@pytest.mark.parametrize("response", ("a", "b"))
def test_response_not_in(response):
    invalid_set = ("b", "c")

    def seed():
        return [Page(Input(validate=validate.response_not_in(invalid_set))), Page()]

    question = make_test_question(seed, response)
    if response in invalid_set:
        assert question.is_valid is False
    else:
        assert question.is_valid is not False


class TestCompareResponse:
    @pytest.mark.parametrize("response", ("a", "b"))
    def test_basic(self, response):
        value = "a"

        def seed():
            return [
                Page(Input(validate=validate.compare_response(value))),
                Page(),
            ]

        question = make_test_question(seed, response)
        if response == value:
            assert question.is_valid is not False
        else:
            assert question.is_valid is False

    @pytest.mark.parametrize("response", ("a", "b"))
    def test_value_as_question(self, response):
        value = "a"

        def seed():
            return [
                Page(
                    input := Input(test_response=value),
                    Input(
                        validate=validate.compare_response(input),
                        test_response=response,
                    ),
                ),
                Page(),
            ]

        create_test_app()
        user = User.make_test_user(seed)
        user.test_request()
        question = user.get_tree().branch[0].questions[1]

        if response == value:
            assert question.is_valid is not False
        else:
            assert question.is_valid is False

    @pytest.mark.parametrize(
        "response, comparison", product((-1, 0, 1), ("<", "<=", "==", "!=", ">=", ">"))
    )
    def test_comparison_operators(self, response, comparison):
        value = 0

        def seed():
            return [
                Page(
                    Input(
                        input_tag={"type": "number"},
                        validate=validate.compare_response(
                            value, comparison=comparison
                        ),
                        test_response=response,
                    )
                ),
                Page(),
            ]

        string_to_operator = {
            "<": operator.lt,
            "<=": operator.le,
            "==": operator.eq,
            "!=": operator.ne,
            ">=": operator.ge,
            ">": operator.gt,
        }
        question = make_test_question(seed, response)
        if string_to_operator[comparison](response, value):
            assert question.is_valid is not False
        else:
            assert question.is_valid is False

    @pytest.mark.parametrize("response", ("01234", "012345"))
    def test_length(self, response):
        value = 5

        def seed():
            return [
                Page(
                    Input(
                        validate=validate.compare_response(value, how="length"),
                    )
                ),
                Page(),
            ]

        question = make_test_question(seed, response)
        if len(response) == value:
            assert question.is_valid is not False
        else:
            assert question.is_valid is False

    @pytest.mark.parametrize("response", ("one", "two words"))
    def test_word_count(self, response):
        value = 1

        def seed():
            return [
                Page(
                    Input(validate=validate.compare_response(value, how="word count"))
                ),
                Page(),
            ]

        question = make_test_question(seed, response)
        if len(re.findall(r"\w+", response)) == value:
            assert question.is_valid is not False
        else:
            assert question.is_valid is False

    @pytest.mark.parametrize("response", ("1", "1.00"))
    def test_decimals(self, response):
        value = 2

        def seed():
            return [
                Page(
                    Input(
                        input_tag={"type": "number"},
                        validate=validate.compare_response(value, how="decimals"),
                    )
                ),
                Page(),
            ]

        question = make_test_question(seed, response)
        if -Decimal(response).as_tuple().exponent == value:
            assert question.is_valid is not False
        else:
            assert question.is_valid is False


@pytest.mark.parametrize(
    "response", ("one", "two words", "three word response", "a four word response")
)
def test_response_in_range(response):
    minwords, maxwords = 2, 3

    def seed():
        return [
            Page(
                Input(
                    validate=validate.response_in_range(
                        minwords, maxwords, how="word count"
                    )
                )
            ),
            Page(),
        ]

    question = make_test_question(seed, response)
    if minwords <= len(re.findall(r"\w+", response)) <= maxwords:
        assert question.is_valid is not False
    else:
        assert question.is_valid is False


@pytest.mark.parametrize("response", ("hello world", "goodbye world"))
def test_re_full_match(response):
    pattern = r"hello *"

    def seed():
        return [Page(Input(validate=validate.re_full_match(pattern))), Page()]

    question = make_test_question(seed, response)
    if re.fullmatch(pattern, response):
        assert question.is_valid is not False
    else:
        assert question.is_valid is False
