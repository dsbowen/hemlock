import pytest

from hemlock.questions import Select

class TestSetIsValid:
    input_valid_class, input_invalid_class = "is-valid", "is-invalid"
    feedback_valid_class, feedback_invalid_class = (
        "valid-feedback",
        "invalid-feedback",
    )

    @pytest.mark.parametrize("is_valid", (None, True, False))
    def test_set_is_valid(self, is_valid):
        valid_class, invalid_class = "is-valid", "is-invalid"

        question = Select()
        question.set_is_valid(is_valid)
        classes = question.select_tag["class"]

        if is_valid is None:
            assert valid_class not in classes
            assert invalid_class not in classes
        elif is_valid:
            assert valid_class in classes
            assert invalid_class not in classes
        else:
            # is_valid is False
            assert valid_class not in classes
            assert invalid_class in classes
