from __future__ import annotations

from typing import Any

import pandas as pd
from flask import render_template


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
