"""Data frame.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Any, Mapping

from sqlalchemy_mutable.utils import is_instance


class DataFrame(defaultdict):
    """Data frame.

    Subclasses :class:`defaultdict`.

    Args:
        data (Mapping, optional): Data contained in the dataframe. Defaults to None.
        fill_rows (bool, optional): Indicates that rows should be filled. Defaults to
            False.

    Notes:

        "Indicates that rows should be filled" means that, when the data frame is
        extended, columns with ``filled == True`` should fill the additional rows with
        the last entry in that column, as opposed to None.

        .. doctest::

            >>> from hemlock._data_frame import DataFrame
            >>> df = DataFrame({"variable": "data"})
            >>> df.pad(3)
            >>> dict(df)
            {'variable': ['data', None, None]}
            >>> df = DataFrame({"variable": "data"}, fill_rows=True)
            >>> df.pad(3)
            >>> dict(df)
            {'variable': ['data', 'data', 'data']}
    """

    def __init__(self, data: Mapping = None, fill_rows: bool = False):
        super().__init__(lambda: Variable())
        if data is not None:
            self.add_data(data, fill_rows)

    def __setitem__(self, key, value):
        return super().__setitem__(key, Variable(value))

    def add_branch(self, branch: List["hemlock.page.Page"]) -> None:  # type: ignore
        """Add data from a given branch to the data frame.

        Args:
            branch (List[Page]): Branch.
        """
        for page in branch:
            self.add_page(page)

    def add_page(self, page: "hemlock.page.Page") -> None:  # type: ignore
        """Add data from a given page to the data frame.

        Args:
            page (Page): Page.
        """
        data_items = [page.timer] + page.data + page.questions
        for item in data_items:
            if item.variable:
                self.add_data(item.pack_data(), item.fill_rows)

    def add_data(self, data: Mapping, fill_rows: bool = False) -> None:
        """Add data from a mapping to the data frame.

        Args:
            data (Mapping): Data.
            fill_rows (bool, optional): Indicates that rows should be filled. Defaults
                to False.
        """
        if not is_instance(data, dict):
            data = dict(data)
        pad_to_row = max([len(self[key]) for key in data.keys()])
        for key, item in data.items():
            self[key].add_data(item, fill_rows, pad_to_row)

    def pad(self, min_rows: int = None) -> None:
        """Pad the data frame so that all variables have the same number of rows.

        Args:
            min_rows (int, optional): Minimum number of rows to pad the variables to.
                Defaults to None.
        """
        if self:
            pad_to_row = max([len(item) for item in self.values()])
            if min_rows is not None:
                pad_to_row = max(min_rows, pad_to_row)
            [item.pad(pad_to_row) for item in self.values()]


class Variable(list):
    """Stores the data for one variable (column) of the :class:`DataFrame`.

    Subclasses :class:`list`.

    Attributes:
        fill_rows (bool): Indicates that rows should be filled.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill_rows = False

    def add_data(
        self, data: Any, fill_rows: bool = False, pad_to_row: int = None
    ) -> None:
        """Add data to this column.

        Args:
            data (Any): Data to add.
            fill_rows (bool, optional): Indicates that rows should be filled. Defaults
                to False.
            pad_to_row (int, optional): If not None, pad the data to this number of
                rows before inserting new data. Defaults to None.
        """
        if pad_to_row is not None:
            self.pad(pad_to_row)

        if not is_instance(data, list):
            data = [data]
        self += [str(item) if isinstance(item, datetime) else item for item in data]

        self.fill_rows = fill_rows

    def pad(self, pad_to_row: int) -> None:
        """Pad the column to a given length.

        Args:
            pad_to_row (int): Length of the column after padding.

        Raises:
            ValueError: ``pad_to_row`` must be at least the current column length.
        """
        n_additional_rows = pad_to_row - len(self)
        if n_additional_rows < 0:
            raise ValueError(
                f"Attempted to pad variable in {pad_to_row} but the variable has {len(self)} rows already."
            )
        padding_data = self[-1] if self.fill_rows and len(self) > 0 else None
        self += n_additional_rows * [padding_data]
