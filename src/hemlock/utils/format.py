from __future__ import annotations

from markdown import markdown


def convert_markdown(value: str, strip_last_paragraph: bool = False) -> str:
    html = markdown(value)

    if not strip_last_paragraph:
        return html

    lines = html.splitlines()
    if lines[-1].startswith("<p>"):
        lines[-1] = lines[-1][len("<p>") : -len("</p>")]
    return "\n".join(lines)
