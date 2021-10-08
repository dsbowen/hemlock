from __future__ import annotations

from itertools import cycle, product
from random import choice, choices, shuffle
from string import digits, ascii_letters
from typing import TYPE_CHECKING, Dict, Iterable, Mapping, Tuple

from flask_login import current_user

if TYPE_CHECKING:
    from ..user import User

CHARACTERS = digits + ascii_letters


def make_hash(length: int = 10) -> str:
    """Make a random hash (can be used as HTML tag id).

    Args:
        length (int, optional): Length of the hash. Defaults to 10.

    Returns:
        str: Hash.
    """
    # the first character must be a letter to be a valid HTML tag id
    return f"{choice(ascii_letters)}{''.join(choices(CHARACTERS, k=length-1))}"


def make_assigner(conditions: Mapping) -> Tuple[Iterable, cycle]:
    """Make an assigner.

    The assigner is passed to :func:`assign_user` to assign a user to conditions.

    Args:
        conditions (Mapping): Maps condition names to possible assigment values.

    Returns:
        Tuple[Iterable, cycle]: Assigner.

    Examples:

        .. code-block::

            >>> from hemlock import User, Page, create_test_app
            >>> from hemlock.utils.random import assign_user, make_assigner
            >>> assigner = make_assigner(
            ...     {"factor0": (0, 1), "factor1": ("low", "medium", "high")}
            ... )
            >>> def seed():
            ...     assignment = assign_user(assigner)
            ...     print("This user was assigned to conditions", assignment)
            ...     return Page()
            ...
            >>> app = create_test_app()
            >>> user = User.make_test_user(seed)
            This user was assigned to conditions {'factor0': 1, 'factor1': 'high'}
            >>> # the user's conditions are automatically stored in their metadata
            >>> user.get_meta_data()["factor0"], user.get_meta_data()["factor1"]
            (1, 'high')
    """
    possible_assignments = list(product(*dict(conditions).values()))
    shuffle(possible_assignments)
    return conditions.keys(), cycle(possible_assignments)


def assign_user(assigner: Tuple[Iterable, cycle], user: User = None) -> Dict:
    """Assign a user to conditions.

    Args:
        assigner (Tuple[Iterable, cycle]): See :func:`make_assigner`.
        user (User, optional): User to assign. Defaults to None.

    Returns:
        Dict: Maps condition names to assignment values.
    """
    if user is None:
        user = current_user
    keys, possible_assignments = assigner
    assignment = {key: value for key, value in zip(keys, next(possible_assignments))}
    user.meta_data.update(assignment)
    return assignment
