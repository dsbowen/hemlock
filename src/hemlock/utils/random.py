"""Randomization.
"""
from __future__ import annotations

from itertools import product
from random import choice, choices
from string import digits, ascii_letters
from typing import TYPE_CHECKING, Any, Mapping

import numpy as np
import pandas as pd
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


class Assigner:
    """Random assigner.

    Args:
        conditions (Mapping): Maps factor names to possible factor values.

    Attributes:
        factor_names (list): Factor names.
        possible_assignments (list[tuple]): Possible factor values to which users may be assigned.

    Examples:

        .. code-block::

            >>> from hemlock import User, Page, create_test_app
            >>> from hemlock.utils.random import Assigner
            >>> assigner = Assigner(
            ...     {"factor0": (0, 1), "factor1": ("low", "medium", "high")}
            ... )
            >>> def seed():
            ...     assignment = assigner.assign_user()
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

    def __init__(self, conditions: Mapping):
        conditions = dict(conditions)
        self.factor_names: list = list(conditions.keys())
        self.possible_assignments: list[tuple] = list(product(*conditions.values()))

    def _decode_numpy(self, value: Any) -> Any:
        """Converts numpy values for JSON serialization.

        Args:
            value (Any): Value to be decoded.

        Returns:
            Any: Decoded value.
        """
        if isinstance(value, np.integer):
            return int(value)
        if isinstance(value, np.ndarray):
            return list(value)
        return value

    def assign_user(self, user: User = None) -> dict[Any, Any]:
        """Assign a user to conditions.

        Args:
            user (User, optional): User to assign. Defaults to None.

        Returns:
            dict[Any, Any]: Maps factor names to assignment values.
        """
        if user is None:
            user = current_user

        # randomly select a condition with the fewest users
        cum_assigned = self.get_cum_assigned()
        values = (
            cum_assigned[cum_assigned["count"] == cum_assigned["count"].min()]
            .sample()
            .index[0]
        )
        if len(self.factor_names) == 1:
            values = [values]
        assignment = {
            key: self._decode_numpy(value)
            for key, value in zip(self.factor_names, values)
        }
        user.meta_data.update(assignment)
        return assignment

    def get_cum_assigned(self, df: pd.DataFrame = None) -> pd.DataFrame:
        """Get cumulative number of users assigned to each condition.

        Args:
            df (pd.DataFrame, optional): Dataframe of user data. If None, uses the
                `:class:hemlock.user.User` metdata. Defaults to None.

        Returns:
            pd.DataFrame: Cumulative number of users in each condition.
        """
        if df is None:
            from ..user import User

            df = pd.DataFrame([user.get_meta_data() for user in User.query.all()])

        if len(self.factor_names) == 1:
            index = [value[0] for value in self.possible_assignments]
        else:
            index = pd.MultiIndex.from_tuples(
                self.possible_assignments, names=self.factor_names
            )

        count_df = pd.DataFrame(index=index)
        if len(df) > 0 and all([name in df for name in self.factor_names]):
            count_df["count"] = df.groupby(self.factor_names)["id"].count()
            count_df.fillna(0, inplace=True)
        else:
            count_df["count"] = 0

        return count_df
