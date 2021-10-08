import pandas as pd

from hemlock import create_test_app
from hemlock.app import db
from hemlock.questions import Label
from hemlock.questions.base import Question
from hemlock.utils.statics import (
    make_figure,
    pandas_to_html,
    recompile_at_interval,
    recompile_question,
)

# Note: These tests mostly test that the functions run without error.
# See test_gallery for tests of expected behavior.


def test_make_figure():
    create_test_app()
    src = "https://src.html"
    html = make_figure(src)
    assert src in html


def test_pandas_to_html():
    df = pd.DataFrame({"x": [0, 1, 2], "y": [3, 4, 5]})
    pandas_to_html(df)


def test_recompile_at_interval():
    question = recompile_at_interval(5000, Question())
    js = question.html_settings["js"]
    assert "cdn.socket.io" in js[0]["src"]  # socketio javascript
    assert "setInterval" in js[1]  # recompile at interval javascript


class TestRecompileQuestion:
    label = "Label."

    @staticmethod
    def add_label(label):
        label.label = TestRecompileQuestion.label

    def test(self):
        label = Label(compile=self.add_label)
        db.session.add(label)
        db.session.commit()
        try:
            recompile_question({"data": label.hash})
        except RuntimeError:
            # A runtime error is expected because this function attempts a socket 
            # emission outside a namespace.
            # However, the label should still be added
            pass
        assert label.label == self.label
