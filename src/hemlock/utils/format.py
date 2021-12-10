"""Utilities for formatting text.
"""
from __future__ import annotations

from markdown import markdown  # type: ignore


def convert_markdown(value: str, strip_last_paragraph: bool = False) -> str:
    """Convert markdown to HTML.

    Args:
        value (str): Raw markdown.
        strip_last_paragraph (bool, optional): Strip the ``<p>`` tag from the last
        paragraph. This improves the look for label questions. Defaults to False.

    Returns:
        str: HTML.
    """
    if not strip_last_paragraph:
        return markdown(value)

    # remove single newline white spaces
    lines = value.splitlines()
    new_line, new_lines = [], []
    for line in lines:
        if line:
            new_line.append(line)
        else:
            new_lines.append(" ".join(new_line))
            new_line.clear()
    new_lines.append(" ".join(new_line))
    value = "\n\n".join(new_lines)

    # remove <p> tag from last line of HTML
    lines = markdown(value).splitlines()
    if lines[-1].startswith("<p>"):
        lines[-1] = lines[-1][len("<p>") : -len("</p>")]
    return "\n".join(lines)


def plural(number: float, singular_form: str, plural_form: str = None) -> str:
    """Make a word singular or plural depending on the quantity.

    Args:
        number (float): Number of things.
        singular_form (str): Singular form of the word.
        plural_form (str, optional): Plural form of the word. Defaults to None.

    Returns:
        str: Singular or plural form of the word.

    Examples:

        .. doctest::

            >>> from hemlock.utils.format import plural
            >>> plural(1, "dollar")
            'dollar'
            >>> plural(2, "dollar")
            'dollars'
            >>> plural(2, "octopus", "octopodes")
            'octopodes'
    """
    if number == 1:
        return singular_form

    return f"{singular_form}s" if plural_form is None else plural_form
