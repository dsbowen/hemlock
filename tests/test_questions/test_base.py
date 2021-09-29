from itertools import combinations_with_replacement, product

import pytest
from sqlalchemy_mutable.utils import partial

from hemlock import User, Page
from hemlock.app import create_test_app
from hemlock.questions import Check, Input, Label
from hemlock.questions.base import Question

question_classes = [Check, Input, Label]


def test_repr():
    question = Question(
        "Hello, world!", variable="variable_name", default="default value"
    )
    assert repr(question) == "<Question Hello, world! - default: default value>"

    question.raw_response = "user response"
    assert repr(question) == "<Question Hello, world! - response: user response>"


@pytest.mark.parametrize("question_cls", question_classes)
def test_display(question_cls):
    # Note: this function simply tests that the display method runs without error.
    # Run the display method in a notebook to verify expected behavior.
    create_test_app()
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
    assert question.get_default() == None

    question.default = "default"
    question.raw_response = response
    expected_result = question.default if response is None else response
    assert question.get_default() == expected_result


class TestSetIsValid:
    valid_class, invalid_class = "valid-feedback", "invalid-feedback"

    @pytest.mark.parametrize(
        "is_valid0, is_valid1", combinations_with_replacement((None, True, False), r=2)
    )
    def test_set_is_valid(self, is_valid0, is_valid1):
        question = Input()
        question.set_is_valid(is_valid0)
        question.set_is_valid(is_valid1)
        classes = question.html_settings["feedback"]["class"]

        if is_valid1 is None:
            assert self.valid_class not in classes
            assert self.invalid_class not in classes
        elif is_valid1:
            assert self.valid_class in classes
            assert self.invalid_class not in classes
        else:
            # is_valid1 is False
            assert self.valid_class not in classes
            assert self.invalid_class in classes


@pytest.mark.parametrize("question_cls", question_classes)
def test_render(question_cls):
    # Note: this test simply tests that the render method runs without error
    # it does not verify that the resulting HTML gives expected behavior
    create_test_app()
    question_cls().render()


class TestValidation:
    valid_response = "valid response"
    invalid_response = "invalid response"
    invalid_feedback0 = "invalid feedback 0"
    invalid_feedback1 = "invalid feedback 1"
    valid_feedback0 = "valid feedback 0"
    valid_feedback1 = "valid feedback 1"

    @staticmethod
    def seed(*args):
        return [
            Page(Input(validate=partial(TestValidation.validate_func, *args))),
            Page(),
        ]

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
    def test_validation(
        self, enter_valid_response, return_feedback, return_invalid_only
    ):
        user = User.make_test_user(
            partial(TestValidation.seed, return_feedback, return_invalid_only)
        )
        question = user.trees[0].branch[0].questions[0]

        if enter_valid_response:
            response = TestValidation.valid_response
        else:
            response = TestValidation.invalid_response
        user.test_request([response])

        if enter_valid_response:
            if return_invalid_only:
                assert question.is_valid is None
                assert question.feedback is None
            else:
                assert question.is_valid
                if return_feedback:
                    assert question.feedback == TestValidation.valid_feedback0
                else:
                    assert question.feedback is None
        else:
            assert question.is_valid is False
            if return_feedback:
                assert question.feedback == TestValidation.invalid_feedback0
            else:
                assert question.feedback is None

    @staticmethod
    def multiple_validate_funcs_seed():
        return [
            Page(
                Input(
                    validate=[
                        TestValidation.validate_func,
                        TestValidation.second_validation_func,
                    ]
                )
            ),
            Page(),
        ]

    @staticmethod
    def second_validation_func(question):
        if question.response != TestValidation.valid_response:
            return False, TestValidation.invalid_feedback1
        return True, TestValidation.valid_feedback1

    @pytest.mark.parametrize("enter_valid_response", (True, False))
    def test_multiple_validate_funcs(self, enter_valid_response):
        user = User.make_test_user(TestValidation.multiple_validate_funcs_seed)
        question = user.trees[0].branch[0].questions[0]

        if enter_valid_response:
            response = TestValidation.valid_response
        else:
            response = TestValidation.invalid_response
        user.test_request([response])

        if enter_valid_response:
            # expecting feedback from the last validate function
            # note that both validate functions succeed
            assert question.feedback == TestValidation.valid_feedback1
        else:
            # expecting feedback from the first validate function that fails
            assert question.feedback == TestValidation.invalid_feedback0


class TestRecordResponseAndData:
    @pytest.mark.parametrize("response_is_none", (True, False))
    def test(self, response_is_none):
        def seed():
            return [Page(Question()), Page()]

        test_response = "" if response_is_none else "test response"
        user = User.make_test_user(seed)
        user.test_request([test_response])

        question = user.trees[0].branch[0].questions[0]
        expected_result = None if response_is_none else test_response
        assert question.response == expected_result
        assert question.data == expected_result