"""Built-in compile functions.
"""
from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING, Union

from flask.templating import render_template

from .base import Functional

if TYPE_CHECKING:
    from ..page import Page
    from ..questions.base import Question

compile = Functional()


@compile.register
def auto_advance(
    obj: Union["Page", "Question"],
    after: int,
    clock_id: str = None,
    clock_update_interval: int = 1000,
) -> None:
    """Automatically advance to the next page after a given amount of time.

    Args:
        obj (Union[): Page or question.
        after (int): Time after which the user will automatically advance
            (milliseconds).
        clock_id (str, optional): ID of an HTML element whose text will be updated with
            the countdown. Defaults to None.
        clock_update_interval (int, optional): Interval of time with which the countdown
            should be updated (milliseconds). Defaults to 1000.

    Examples:
        Copy and paste the following into a python file, then run it. This will display
        a countdown and automatically advance the user after 10 seconds (10000
        milliseconds).

        .. code-block::

            from hemlock import User, Page, create_app
            from hemlock.functional import compile
            from hemlock.questions import Label

            @User.route("/survey")
            def seed():
                return [
                    Page(
                        Label(
                            "Remaining time: <span id='clock-id'></span>",
                            compile=compile.auto_advance(10000, clock_id="clock-id")
                        ),
                    ),
                    Page(
                        Label("The End."),
                    )
                ]

            app = create_app()

            if __name__ == "__main__":
                app.run()
    """
    # remove any auto-advance javascript from running this function previously
    obj.html_settings["js"] = [
        js
        for js in obj.html_settings["js"]
        if not js.startswith("<script id=\"auto-advance\"")
    ]
    obj.html_settings["js"].append(
        render_template(
            "hemlock/statics/auto_advance.html",
            start_time=datetime.utcnow().isoformat(),
            after=after,
            clock_id=clock_id,
            clock_update_interval=clock_update_interval,
        )
    )


@compile.register
def clear_feedback(obj: Union["Page", "Question"]) -> None:
    """Clear feedback.

    Args:
        obj (Union[Page, Question]): Page or question whose feedback will be cleared.
    """
    obj.clear_feedback()


@compile.register
def clear_response(obj: Union["Page", "Question"]) -> None:
    """Clear response.

    Args:
        obj (Union[Page, Question]): Page or question whose responses will be cleared.
    """
    obj.clear_response()
