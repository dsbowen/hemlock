from datetime import datetime
from itertools import combinations_with_replacement

import pytest

from hemlock.questions import Input
from hemlock.questions.input import datetime_input_types

now = datetime.utcnow()


class TestResponseConversion:
    # maps input type to (raw response, expected response type)
    type_response_mapping = {"text": ("text response", str), "number": ("1", float)}
    datetime_response_mapping = {
        key: (now.strftime(item[1]), datetime)
        for key, item in datetime_input_types.items()
    }
    type_response_mapping.update(datetime_response_mapping)

    @pytest.mark.parametrize("input_type", type_response_mapping.keys())
    def test_response_conversion(self, input_type):
        question = Input(input_tag={"type": input_type})
        # test response before user has responded
        assert question.response is None

        # test response if user did not respond
        question.raw_response = ""
        assert question.response is None

        # test response after user has responded
        response, expected_type = self.type_response_mapping[input_type]
        question.raw_response = response
        assert isinstance(question.response, expected_type)

    @pytest.mark.parametrize("input_type", type_response_mapping.keys())
    def test_validation(self, input_type):
        # test that validation functions will indicate an invalid response when the
        # response type is incorrect
        question = Input(input_tag={"type": input_type})

        # test that validate functions will not indicate an invalid response when no
        # response was given
        assert question.run_validate_functions()
        question.raw_response = ""
        assert question.run_validate_functions()

        question.raw_response = "text response"
        if input_type == "text":
            # validate functions should indicate a valid response when expecting a text
            # response
            assert question.run_validate_functions()
            assert question.is_valid is None
            assert question.feedback is None
        else:
            # validate functions should indicate an incorrect response otherwise
            assert not question.run_validate_functions()
            assert question.is_valid is False
            assert question.feedback is not None


class TestSetIsValid:
    input_valid_class, input_invalid_class = "is-valid", "is-invalid"
    feedback_valid_class, feedback_invalid_class = (
        "valid-feedback",
        "invalid-feedback",
    )

    @pytest.mark.parametrize(
        "is_valid0, is_valid1", combinations_with_replacement((None, True, False), r=2)
    )
    def test_set_is_valid(self, is_valid0, is_valid1):
        question = Input()
        question.set_is_valid(is_valid0)
        question.set_is_valid(is_valid1)
        input_classes = question.input_tag["class"]
        feedback_classes = question.html_settings["feedback"]["class"]

        if is_valid1 is None:
            assert self.input_valid_class not in input_classes
            assert self.input_invalid_class not in input_classes
            assert self.feedback_valid_class not in feedback_classes
            assert self.feedback_invalid_class not in feedback_classes
        elif is_valid1:
            assert self.input_valid_class in input_classes
            assert self.input_invalid_class not in input_classes
            assert self.feedback_valid_class in feedback_classes
            assert self.feedback_invalid_class not in feedback_classes
        else:
            # is_valid1 is False
            assert self.input_valid_class not in input_classes
            assert self.input_invalid_class in input_classes
            assert self.feedback_valid_class not in feedback_classes
            assert self.feedback_invalid_class in feedback_classes
