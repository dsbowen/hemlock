import pytest

from sqlalchemy_mutable.utils import partial

from hemlock import User, Page, create_test_app
from hemlock.questions import Check
from hemlock.questions.choice_base import ChoiceQuestion


def make_question(default=None, response=None, multiple=False):
    question = ChoiceQuestion(
        "Hello, world!",
        [0, "value 1", (2, "label 2")],
        default=default,
        multiple=multiple,
    )
    question.raw_response = response
    return question


class TestResponse:
    @pytest.mark.parametrize("multiple", (True, False))
    def test_no_response(self, multiple):
        question = ChoiceQuestion(multiple=multiple)
        question.raw_response = []
        if multiple:
            assert question.response == []
        else:
            assert question.response is None

    def test_single_choice(self):
        choice_value = "choice_value"
        question = ChoiceQuestion()
        question.raw_response = [choice_value]
        assert question.response == choice_value

    @pytest.mark.parametrize("choice_values", ([0], [0, 1]))
    def test_multi_choice(self, choice_values):
        question = ChoiceQuestion(multiple=True)
        question.raw_response = choice_values
        assert question.response == choice_values


class TestRepr:
    def test_without_choices(self):
        question = ChoiceQuestion("Hello, world!")
        assert repr(question) == "<ChoiceQuestion Hello, world! - default: None>"

    def test_with_choices(self):
        question = make_question()
        for choice in question.choices:
            assert str(choice["value"]) in repr(question)

    def test_with_many_choices(self):
        question = ChoiceQuestion("Hello, world!", list(range(100)))
        # test that repr doesn't display all the choice values
        assert str(question.choices[-1]["value"]) not in repr(question)
        assert "[...]" in repr(question)


class TestIsDefault:
    def test_default_is_none(self):
        question = make_question()
        assert not any([question.is_default(choice) for choice in question.choices])

    def test_single_choice(self):
        question = make_question(default=0)
        assert question.is_default(question.choices[0])
        assert not any([question.is_default(choice) for choice in question.choices[1:]])

    def test_multiple_choices(self):
        question = make_question(default=["value 1", 2], multiple=True)
        assert not question.is_default(question.choices[0])
        assert all([question.is_default(choice) for choice in question.choices[1:]])

    def test_after_no_response(self):
        question = make_question(default=0, response=[])
        assert not question.is_default(question.choices[0])

    def test_after_single_response(self):
        question = make_question(default="value 1", response=[2])
        assert not any([question.is_default(choice) for choice in question.choices[:2]])
        assert question.is_default(question.choices[2])

    def test_after_multiple_responses(self):
        question = make_question(default=[2], response=[0, "value 1"], multiple=True)
        assert all([question.is_default(choice) for choice in question.choices[:2]])
        assert not question.is_default(question.choices[2])


class TestRecordResponseAndData:
    variable = "variable"

    def make_question(self, response, multiple=False):
        def seed(multiple):
            return [
                Page(
                    Check(
                        "Hello, world!",
                        [0, "value 1", (2, "value 2")],
                        multiple=multiple,
                    ),
                ),
                Page(),
            ]

        create_test_app()
        user = User.make_test_user(partial(seed, multiple))
        return user.test_request([response]).branch[0].questions[0]

    def assert_correct_packed_data(self, question, expected_packed_data):
        assert question.pack_data() == {}

        question.variable = self.variable
        assert question.pack_data() == expected_packed_data

        question.record_choice_indices = True
        expected_packed_data.update(
            {
                f"{self.variable}_0_index": [0],
                f"{self.variable}_value 1_index": [1],
                f"{self.variable}_2_index": [2],
            }
        )
        assert question.pack_data() == expected_packed_data

    def test_response_is_none(self):
        response = None
        question = self.make_question(response)
        assert question.raw_response == []
        assert question.response is None
        assert question.data is None
        self.assert_correct_packed_data(question, {self.variable: [response]})

    def test_single_response(self):
        response = 0
        question = self.make_question(response)
        assert question.raw_response == [0]
        assert question.response == 0
        assert question.data == 0
        self.assert_correct_packed_data(question, {self.variable: [response]})

    def test_multiple_response_is_none(self):
        question = self.make_question(None, multiple=True)
        assert question.raw_response == []
        assert question.response == []
        assert question.data == {0: 0, "value 1": 0, 2: 0}
        self.assert_correct_packed_data(
            question,
            {
                f"{self.variable}_0": [0],
                f"{self.variable}_value 1": [0],
                f"{self.variable}_2": [0],
            },
        )

    def test_multiple_response(self):
        question = self.make_question((0, "value 1"), multiple=True)
        assert question.raw_response == [0, "value 1"]
        assert question.response == [0, "value 1"]
        assert question.data == {0: 1, "value 1": 1, 2: 0}
        self.assert_correct_packed_data(
            question,
            {
                f"{self.variable}_0": [1],
                f"{self.variable}_value 1": [1],
                f"{self.variable}_2": [0],
            },
        )
