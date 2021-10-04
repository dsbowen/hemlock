import pytest

from hemlock import create_test_app
from hemlock.questions import Range


@pytest.mark.parametrize("min_value, max_value", ((0, 100), (101, 200)))
def test_response(min_value, max_value):
    create_test_app()
    question = Range(input_tag={"min": min_value, "max": max_value})
    response = question.test_response(question)
    raw_response = question.make_raw_test_response(response)
    assert isinstance(raw_response, str)
    question.raw_response = raw_response
    assert isinstance(question.response, float)
    assert min_value <= question.response <= max_value
