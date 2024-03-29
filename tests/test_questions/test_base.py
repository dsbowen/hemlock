from itertools import combinations_with_replacement, product

import pytest
from sqlalchemy_mutable.utils import partial

from hemlock import User, Page
from hemlock.questions import Check, Input, Label, Range, Select, Textarea
from hemlock.questions.base import Question

from . import utils
from ..utils import app

question_classes = [Check, Input, Label, Range, Select, Textarea]


def test_repr():
    question = Question(
        "Hello, world!", variable="variable_name", default="default value"
    )
    assert repr(question) == "<Question Hello, world! - default: 'default value'>"

    question.raw_response = "user response"
    assert repr(question) == "<Question Hello, world! - response: 'user response'>"


@pytest.mark.parametrize("question_cls", question_classes)
def test_display(app, question_cls):
    # Note: this function simply tests that the display method runs without error.
    # Run the display method in a notebook to verify expected behavior.
    question_cls().display()


def test_clear_feedback():
    question = Question()

    question.feedback = "here is some feedback"
    question.set_is_valid(True)
    assert question.is_valid is True

    question.clear_feedback()
    assert question.feedback is None
    assert question.is_valid is None


def test_clear_response():
    question = Question()

    question.raw_response = "user response"
    question.feedback = "here is some feedback"
    question.set_is_valid(False)
    assert question.is_valid is False

    question.clear_response()
    assert question.raw_response is None
    assert question.feedback is None
    assert question.is_valid is None


@pytest.mark.parametrize("response", (None, "", "response"))
def test_get_default(response):
    question = Question()
    assert question.get_default() is None
    alt_value = "alternative value"
    assert question.get_default(alt_value) == alt_value

    question.default = "default"
    question.raw_response = response
    expected_result = question.default if response is None else response
    assert question.get_default() == expected_result


@pytest.mark.parametrize(
    "is_valid0, is_valid1", combinations_with_replacement((None, True, False), r=2)
)
def test_set_is_valid(is_valid0, is_valid1):
    utils.test_set_is_valid(
        is_valid0, is_valid1, Question, "feedback", "valid-feedback", "invalid-feedback"
    )


@pytest.mark.parametrize("question_cls", question_classes)
def test_render(app, question_cls):
    # Note: this test simply tests that the render method runs without error
    # it does not verify that the resulting HTML gives expected behavior
    question_cls().render()


class TestValidation:
    valid_response = "valid response"
    invalid_response = "invalid response"
    invalid_feedback0 = "invalid feedback 0"
    invalid_feedback1 = "invalid feedback 1"
    valid_feedback0 = "valid feedback 0"
    valid_feedback1 = "valid feedback 1"

    @staticmethod
    def validate_func(question, return_feedback=True, return_invalid_only=False):
        if question.response != TestValidation.valid_response:
            if return_feedback:
                return False, TestValidation.invalid_feedback0
            return False

        if return_invalid_only:
            return None

        if return_feedback:
            return True, TestValidation.valid_feedback0
        return True

    @pytest.mark.parametrize(
        "enter_valid_response, return_feedback, return_invalid_only",
        product((True, False), (True, False), (True, False)),
    )
    def test_single_func(
        self, enter_valid_response, return_feedback, return_invalid_only
    ):
        def seed(*args):
            return [
                Page(Input(validate=partial(self.validate_func, *args))),
                Page(),
            ]

        user = User.make_test_user(partial(seed, return_feedback, return_invalid_only))
        question = user.get_tree().branch[0].questions[0]

        if enter_valid_response:
            response = self.valid_response
        else:
            response = self.invalid_response
        user.test_request([response])

        if enter_valid_response:
            if return_invalid_only:
                assert question.is_valid is None
                assert question.feedback is None
            else:
                assert question.is_valid
                if return_feedback:
                    assert question.feedback == self.valid_feedback0
                else:
                    assert question.feedback is None
        else:
            assert question.is_valid is False
            if return_feedback:
                assert question.feedback == self.invalid_feedback0
            else:
                assert question.feedback is None

    @staticmethod
    def second_validation_func(question):
        if question.response != TestValidation.valid_response:
            return False, TestValidation.invalid_feedback1
        return True, TestValidation.valid_feedback1

    @pytest.mark.parametrize("enter_valid_response", (True, False))
    def test_multiple_funcs(self, enter_valid_response):
        def seed():
            return [
                Page(Input(validate=[self.validate_func, self.second_validation_func])),
                Page(),
            ]

        user = User.make_test_user(seed)
        question = user.get_tree().branch[0].questions[0]

        if enter_valid_response:
            response = self.valid_response
        else:
            response = self.invalid_response
        user.test_request([response])

        if enter_valid_response:
            # expecting feedback from the last validate function
            # note that both validate functions succeed
            assert question.feedback == self.valid_feedback1
        else:
            # expecting feedback from the first validate function that fails
            assert question.feedback == self.invalid_feedback0


@pytest.mark.parametrize("test_response", (None, "test response"))
def test_record_response_and_data(test_response):
    def seed():
        return [Page(Question()), Page()]

    user = User.make_test_user(seed)
    user.test_request([test_response])

    question = user.get_tree().branch[0].questions[0]
    assert question.response == test_response
    assert question.data == test_response
