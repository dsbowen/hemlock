"""A class for registering functions.
"""
from __future__ import annotations

import functools
from typing import Any, Callable, List, Tuple, Union

from sqlalchemy_mutable.utils import partial


class Functional(dict):
    """A class for registering functions.

    Attributes:
        functions (Dict[str, Callable]): Registered functions.

    Examples:
        Accessing registered functions is similar to accessing columns in a pandas
        DataFrame. If you access a function with a tuple, the first item of the tuple is
        understood as the key, while the rest of tuple items are passed to the function
        as arguments.

        .. code-block::

            >>> from hemlock.functional import Functional
            >>> functional = Functional()
            >>> @functional.register
            ... def foo(*args):
            ...     pass
            ...
            >>> functional.foo("Hello, world!")
            <foo('Hello, world!')>
            >>> functional["foo"]
            <foo()>
            >>> functional[["foo", "foo"]]
            [<foo()>, <foo()>]
            >>> functional[("foo", "Hello, world!")]
            <foo('Hello, world!')>
            >>> functional[[("foo", "Hello, world!"), ("foo", "Goodbye, world!")]]
            [<foo('Hello, world!')>, <foo('Goodbye, world!')>]
    """

    def register(self, func: Callable) -> Callable:
        """Decorator to register a new function.

        Args:
            func (Callable): Function to be registered.

        Returns:
            Callable: Original function.
        """

        @functools.wraps(func)
        def make_partial(*args, **kwargs):
            return partial(func, *args, **kwargs)

        self[func.__name__] = make_partial
        return func

    def __getattribute__(self, name: str) -> Any:
        try:
            return super().__getattribute__(name)
        except AttributeError:
            return super().__getitem__(name)

    def __getitem__(
        self, keys: Union[str, Tuple, List[str], List[Tuple]]
    ) -> Union[partial, List[partial]]:
        if isinstance(keys, list):
            return_value = []
            for key in keys:
                if isinstance(key, tuple):
                    return_value.append(super().__getitem__(key[0])(*key[1:]))
                else:
                    return_value.append(super().__getitem__(key)())
            return return_value

        if isinstance(keys, tuple):
            return super().__getitem__(keys[0])(*keys[1:])
        return super().__getitem__(keys)()
