from itertools import combinations_with_replacement, product
from random import random

import pytest
from sqlalchemy_mutable.utils import partial

from hemlock import User, Tree, Page
from hemlock.app import create_test_app
from hemlock.data import Data
from hemlock.questions import Input, Label
from hemlock.questions.base import Question
from hemlock.timer import Timer


@pytest.mark.parametrize("timer", (None, "seconds", Timer("seconds")))
def test_timer_setting(timer):
    # test that the timer can be initialized with None, str, or Timer
    page = Page(timer=timer)
    if timer is None:
        assert page.timer.variable is None
    elif isinstance(timer, str):
        assert page.timer.variable == timer
    else:
        assert page.timer is timer


@pytest.mark.parametrize("as_data", (True, False))
def test_data_validation(as_data):
    # test that data can be input as Data object or tuple of arguments to Data
    # constructor
    variable_name, variable_data = "variable", "data"
    data = (variable_name, variable_data)
    if as_data:
        data = Data(*data)
    page = Page(data=[data])
    assert page.data[0].variable == variable_name
    assert page.data[0].data == variable_data


@pytest.mark.parametrize("value", ("", None, False, True, "Button text"))
def test_direction_validation(value):
    page = Page()
    page.forward = page.back = value
    if value in ("", None, False):
        assert page.forward is None and page.back is None
    elif value is True:
        assert page.forward == ">>"
        assert page.back == "<<"
    else:
        assert page.forward == page.back == value


@pytest.mark.parametrize("root_is_tree", (True, False))
def test_root_branch(root_is_tree):
    def seed():
        return Page()

    if root_is_tree:
        root = Tree(seed)
        page = root.branch[0]
    else:
        root = Page()
        root.branch = [page := Page()]

    assert page.root_branch is root.branch


class TestPosition:
    n_pages = 6  # number of pages in test survey

    def get_user(self):
        def seed():
            return [Page(navigate=self.make_next_branch), Page()]

        create_test_app()
        return User.make_test_user(seed)

    @staticmethod
    def make_next_branch(root):
        return [
            Page(navigate=TestPosition.make_next_next_branch),
            Page(navigate=TestPosition.make_next_next_branch),
        ]

    @staticmethod
    def make_next_next_branch(root):
        return Page()

    def test_is_first_page(self):
        user = self.get_user()

        # test that first page is first page
        assert user.test_get().page.is_first_page

        for _ in range(self.n_pages - 1):
            # go forward until last page,
            # checking that each subsequent page is not the first
            assert not user.test_request().page.is_first_page

    def test_is_last_page(self):
        user = self.get_user()

        # test that the first page is not the last page
        assert not user.test_get().page.is_last_page

        for _ in range(self.n_pages - 2):
            # test that the next 2 pages are not the last page
            assert not user.test_request().page.is_last_page

        # test that the last page is the last page
        assert user.test_request().page.is_last_page

    def test_terminal_page(self):
        # test that a page explicitly marked as terminal is the last page
        assert Page(terminal=True).is_last_page

    def test_unattached_page(self):
        # test that pages without roots are neither first nor last
        page = Page()
        assert not page.is_first_page
        assert not page.is_last_page

    def test_position(self):
        user = self.get_user()

        assert user.test_get().page.get_position() == "0"

        expected_results = ["0.0", "0.0.0", "0.1", "0.1.0", "1"]
        for expected_result in expected_results:
            assert user.test_request().page.get_position() == expected_result


@pytest.mark.parametrize(
    "question_is_valid", combinations_with_replacement((None, True, False), r=3)
)
def test_is_valid(question_is_valid):
    page = Page(*[Question() for _ in question_is_valid])
    for question, is_valid in zip(page.questions, question_is_valid):
        question.set_is_valid(is_valid)
    expected_result = all([is_valid in (True, None) for is_valid in question_is_valid])
    assert page.is_valid is expected_result


class TestRepr:
    def test_unattached(self):
        assert repr(Page()) == "<Page None>"

    def test_page_on_tree(self):
        def seed():
            return [Page(), Page()]

        tree = Tree(seed)
        assert repr(tree.branch[0] == "<Page 0>")
        assert repr(tree.branch[1] == "<Page 1 terminal>")

    def test_page_with_questions(self):
        page = Page(question := Question())
        assert str(question) in repr(page)

    def test_with_test_responses(self):
        test_response, direction = "test response", "forward"
        page = Page(question := Question())
        string = page.print({question: test_response}, direction=direction)
        assert test_response in string
        assert direction in string


def test_display():
    # Note: this function simply tests that the display method runs without error.
    # Run the display method in a notebook to verify expected behavior.
    Page().display()


def test_clear_feedback():
    page = Page(*[Question() for _ in range(3)])

    question = page.questions[0]
    question.set_is_valid(False)
    question.feedback = "Here is some feedback."

    question = page.questions[1]
    question.set_is_valid(True)

    page.clear_feedback()
    for question in page.questions:
        assert question.is_valid is None
        assert question.feedback is None


def test_clear_response():
    page = Page(*[Question() for _ in range(3)])

    question = page.questions[0]
    question.raw_response = "Raw response."
    question.set_is_valid(False)
    question.feedback = "Here is some feedback."

    question = page.questions[1]
    question.raw_response = "Raw response."
    question.set_is_valid(True)

    page.questions[2].raw_response = "Raw response."

    page.clear_response()
    for question in page.questions:
        assert question.raw_response is None
        assert question.is_valid is None
        assert question.feedback is None


def test_render():
    # Note: this test simply tests that the render method runs without error
    # it does not verify that the resulting HTML gives expected behavior
    Page().render()


class TestGet:
    @staticmethod
    def change_label(question, new_label):
        question.label = new_label

    @pytest.mark.parametrize(
        "direction_to, rerun_compile_functions",
        product(("forward", "back", "invalid"), (True, False)),
    )
    def test_compile_functions(self, direction_to, rerun_compile_functions):
        original_label, new_label = "Original label.", "New label."
        page = Page(
            question := Label(
                original_label, compile=partial(self.change_label, new_label)
            ),
            rerun_compile_functions=rerun_compile_functions,
        )

        page.direction_to = direction_to
        page.get()
        assert page.timer.is_running
        if direction_to in ("forward", None) or rerun_compile_functions:
            assert question.label == new_label
        else:
            assert question.label == original_label


class TestPost:
    valid_response = "Valid repsonse"
    invalid_response = "Invalid response"
    invalid_feedback = "Invalid feedback."

    @staticmethod
    def response_is_valid(question):
        if question.response == TestPost.valid_response:
            return True
        return False, TestPost.invalid_feedback

    # forward versus back or invalid
    # valid versus invalid
    @pytest.mark.parametrize(
        "direction, enter_valid_response, zeroeth_try_is_invalid",
        product(("forward", "back"), (True, False), (True, False)),
    )
    def test_post(self, direction, enter_valid_response, zeroeth_try_is_invalid):
        def seed():
            return [Page(), Page(Input(validate=self.response_is_valid)), Page()]

        # create test user and go to first page
        user = User.make_test_user(seed)
        user.test_get()
        user.test_request()
        if zeroeth_try_is_invalid:
            # user submits an invalid response on the zeroeth try
            user.test_request([self.invalid_response])

        response = (
            self.valid_response if enter_valid_response else self.invalid_response
        )
        tree = user.test_request([response], direction=direction)
        page = tree.branch[1]

        # test that the response was recorded
        assert page.questions[0].response == response

        if direction == "forward":
            if enter_valid_response:
                assert not page.timer.is_running
                assert tree.page is tree.branch[2]
                assert page.direction_from == "forward"
                assert page.is_valid
                assert page.questions[0].feedback is None
                assert page.questions[0].data == self.valid_response
            else:
                # the timer should still be running because the user is on the same page
                assert page.timer.is_running
                assert tree.page is page
                assert page.direction_from == "invalid"
                assert not page.is_valid
                assert page.questions[0].feedback == self.invalid_feedback
                assert page.questions[0].data is None
        elif direction == "back":
            assert not page.timer.is_running
            assert tree.page is tree.branch[0]
            assert page.direction_from == "back"
            # feedback should be stored if the user goes back after entering an invalid response
            expected_feedback = (
                self.invalid_feedback if zeroeth_try_is_invalid else None
            )
            assert page.questions[0].feedback == expected_feedback
            assert page.questions[0].data is None
