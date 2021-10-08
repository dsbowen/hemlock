"""Tools for creating static objects.

Static objects include figures, javascript, and HTML.
"""
from __future__ import annotations

import warnings
from typing import TYPE_CHECKING, Any, Dict

import pandas as pd
from flask import render_template
from flask_socketio import emit

from ..app import db, socketio

if TYPE_CHECKING:
    from ..questions.base import Question


def make_figure(
    src: str,
    caption: str = None,
    alt: str = "alt",
    figure_align: str = "start",
    caption_align: str = "start",
    template: str = "hemlock/statics/figure.html",
) -> str:
    """Insert an figure.

    Args:
        src (str): Image URL.
        caption (str, optional): Caption. Defaults to None.
        alt (str, optional): Alternative text displayed if the image fails to load.
            Defaults to "alt".
        figure_align (str, optional): Figure alignment ("start", "center", "end").
            Defaults to "start".
        caption_align (str, optional): Caption alignment ("start", "center", "end").
            Defaults to "start".
        template (str, optional): Path to Jinja template. Defaults to
            "hemlock/statics/img.html".

    Returns:
        str: Figure tag.

    Examples:

        .. code-block::

            >>> from hemlock import create_test_app
            >>> from hemlock.utils.statics import make_figure
            >>> create_test_app()
            >>> make_figure("https://link-to-image.html")
    """
    return render_template(
        template,
        src=src,
        caption=caption,
        alt=alt,
        figure_align=figure_align,
        caption_align=caption_align,
    )


def pandas_to_html(dataframe: pd.DataFrame, *args: Any, **kwargs: Any) -> str:
    """Convert pandas dataframe to HTML.

    While pandas dataframes have a built-in ``to_html`` method, it doesn't take
    advantage of the additional stylings provided by hemlock pages.

    Args:
        dataframe (pd.DataFrame): Dataframe.
        *args (Any): Passed to ``pd.DataFrame.to_html``.
        **kwargs (Any): Passed to ``pd.DataFrame.to_html``.

    Returns:
        str: HTML.
    """
    default_kwargs = {
        "classes": ["table", "table-striped", "table-hover"],
        "border": 0,
        "justify": "match-parent",
    }
    default_kwargs.update(kwargs)
    return dataframe.to_html(*args, **default_kwargs)


def recompile_at_interval(interval: int, question: "Question") -> "Question":
    """Add javascript to recompile this question at regular intervals.

    That is, at regular intervals, the question's compile functions will be rerun and
    its HTML re-rendered for the user.

    Args:
        interval (int): Recompile interval (milliseconds).
        question (Question): Question which should be recompiled.

    Returns:
        Question: Question from the arguments.
    """
    question.html_settings["js"] += [
        {"src": "https://cdn.socket.io/4.2.0/socket.io.min.js"},
        render_template(
            "hemlock/statics/recompile_at_interval.js",
            hash=question.hash,
            interval=interval,
        )
    ]
    return question


@socketio.on("recompile-question-event")
def recompile_question(question_hash: Dict[str, str]) -> None:
    """Rerun a question's compile functions.

    Args:
        question_hash (Dict[str, str]): Hash of the question to be recompiled
            ({"data": question.hash}).
    """
    from ..questions.base import Question

    hash = question_hash["data"]
    question = Question.query.filter_by(hash=hash).first()
    if question is None:
        warnings.warn(f"Question with hash {hash} does not exist.", RuntimeWarning)
        return None

    question.run_compile_functions()
    db.session.commit()
    emit("recompile-question-response", {"data": question.render()})
