import pytest

from hemlock import Page
from hemlock.functional import compile
from hemlock.questions.base import Question


@pytest.mark.parametrize("from_page", (True, False))
def test_clear_feedback(from_page):
    if from_page:
        object = Page(question := Question())
    else:
        object = question = Question()

    question.set_is_valid(True)
    question.feedback = "Feedback."

    compile.clear_feedback()(object)
    assert question.is_valid is None
    assert question.feedback is None


@pytest.mark.parametrize("from_page", (True, False))
def test_clear_response(from_page):
    if from_page:
        object = Page(question := Question())
    else:
        object = question = Question()

    question.raw_response = "Raw response."
    question.set_is_valid(False)
    question.feedback = "Feedback."

    compile.clear_response()(object)
    assert question.raw_response is None
    assert question.is_valid is None
    assert question.feedback is None
