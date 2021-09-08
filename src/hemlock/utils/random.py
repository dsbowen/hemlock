from __future__ import annotations

from random import choice, choices
from string import digits, ascii_letters

CHARACTERS = digits + ascii_letters


def make_hash(length: int = 10) -> str:
    # the first character must be a letter to be a valid HTML tag id
    return f"{choice(ascii_letters)}{''.join(choices(CHARACTERS, k=length-1))}"
