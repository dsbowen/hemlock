import pytest

from hemlock import Page, create_test_app
from hemlock.functional import compile
from hemlock.questions.base import Question


class TestAutoAdvance:
    def test_basic(self):
        create_test_app()
        question = Question()
        compile.auto_advance(10000)(question)

        found_auto_advance_js = False
        for js in question.html_settings["js"]:
            if js.startswith('<script id="auto-advance"'):
                found_auto_advance_js = True
                break
        assert found_auto_advance_js

    def test_multiple_compile(self):
        # test that rerunning the compile function removes the first auto-advance js
        create_test_app()
        question = Question()
        compile.auto_advance(10000)(question)
        compile.auto_advance(10000)(question)
        n_auto_advance_js = 0
        for js in question.html_settings["js"]:
            if js.startswith('<script id="auto-advance"'):
                n_auto_advance_js += 1
        assert n_auto_advance_js == 1


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
