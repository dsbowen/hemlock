import pytest

from hemlock.questions import Range

from ..utils import app


@pytest.mark.parametrize("min_value, max_value", ((0, 100), (101, 200)))
def test_response(app, min_value, max_value):
    question = Range(input_tag={"min": min_value, "max": max_value})
    response = question.test_response(question)
    raw_response = question.make_raw_test_response(response)
    assert isinstance(raw_response, str)
    question.raw_response = raw_response
    assert isinstance(question.response, float)
    assert min_value <= question.response <= max_value
