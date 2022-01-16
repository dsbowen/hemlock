from multiprocessing.sharedctypes import Value
import pytest

from hemlock.questions import Label


@pytest.mark.parametrize("response", (None, "", "invalid-response"))
def test_make_raw_test_response(response):
    # Label should raise an error when the test user enters a non-empty response
    label = Label()
    if response not in (None, ""):
        with pytest.raises(ValueError):
            label.make_raw_test_response(response)
    else:
        label.make_raw_test_response(response)
