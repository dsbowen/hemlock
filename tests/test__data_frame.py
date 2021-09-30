import pytest

from hemlock import Page
from hemlock._data_frame import DataFrame

VARIABLE = "variable"
DATA = "data"


def test_init():
    assert DataFrame([(VARIABLE, DATA)]) == {VARIABLE: [DATA]}


def test_add_branch():
    # this also tests add_page
    def make_branch():
        return [Page(data=[(VARIABLE, DATA)]) for _ in range(n_pages_per_branch)]

    n_pages_per_branch = 2
    branch = make_branch()
    branch[0].branch = make_branch()
    df = DataFrame()
    df.add_branch(branch)
    assert df == {VARIABLE: 2 * n_pages_per_branch * [DATA]}


@pytest.mark.parametrize("fill_rows", (True, False))
def test_pad(fill_rows):
    min_rows = 3
    df = DataFrame({VARIABLE: DATA}, fill_rows=fill_rows)
    df.pad(min_rows)
    if fill_rows:
        assert df == {VARIABLE: min_rows * [DATA]}
    else:
        assert df == {VARIABLE: [DATA] + (min_rows - 1) * [None]}
