import pandas as pd

from hemlock import create_test_app
from hemlock.utils.statics import make_figure, pandas_to_html

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