from hemlock.functional import Functional


functional = Functional()


@functional.register
def foo(*args, **kwargs):
    return args, kwargs


def test_register():
    assert "foo" in functional


def test_getattribute():
    args, kwargs = (0, 1, 2), {"hello": "world"}
    assert functional.foo(*args, **kwargs)() == (args, kwargs)
    assert functional.foo()(*args, **kwargs) == (args, kwargs)


class TestGetItem:
    def test_from_string(self):
        assert functional["foo"]() == ((), {})

    def test_from_tuple(self):
        assert functional[("foo", 0, 1, 2)]() == ((0, 1, 2), {})

    def test_from_list_of_strings(self):
        for func in functional[["foo", "foo"]]:
            assert func() == ((), {})

    def test_from_list_of_tuples(self):
        for func in functional[[("foo", 0, 1, 2), ("foo", 0, 1, 2)]]:
            assert func() == ((0, 1, 2), {})
