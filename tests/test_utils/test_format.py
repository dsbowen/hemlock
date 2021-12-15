import pytest

from hemlock.utils.format import plural


@pytest.mark.parametrize("number", (1, 2))
@pytest.mark.parametrize(
    "singular_form, plural_form", (("dollar", None), ("octopus", "octopodes"))
)
def test_plural(number, singular_form, plural_form):
    result = plural(number, singular_form, plural_form)
    if singular_form == "dollar":
        expected_result = "dollar" if number == 1 else "dollars"
    else:
        expected_result = "octopus" if number == 1 else "octopodes"

    assert result == expected_result
