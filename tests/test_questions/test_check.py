import pytest

from hemlock.questions import Check


@pytest.mark.parametrize("inline", (None, True, False))
def test_inline(inline):
    inline_class = "form-check-inline"
    check = Check(inline=inline)
    if inline:
        assert inline_class in check.html_settings["div"]["class"]
    else:
        assert inline_class not in check.html_settings["div"]["class"]


@pytest.mark.parametrize("switch", (None, True, False))
def test_switch(switch):
    inline_class = "form-switch"
    check = Check(switch=switch)
    if switch:
        assert inline_class in check.html_settings["div"]["class"]
    else:
        assert inline_class not in check.html_settings["div"]["class"]
