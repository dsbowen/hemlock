from __future__ import annotations

from collections import defaultdict
from datetime import datetime
from typing import Mapping

from sqlalchemy_mutable.utils import is_instance


class DataFrame(defaultdict):
    def __init__(self, data: Mapping = None, fill_rows: bool = False):
        super().__init__(lambda: Variable())
        if data is not None:
            self.add_data(data, fill_rows)

    def __setitem__(self, key, value):
        return super().__setitem__(key, Variable(value))

    def add_branch(self, branch):
        [self.add_page(page) for page in branch]

    def add_page(self, page):
        data_items = [page.timer] + page.data + page.questions
        [
            self.add_data(item.pack_data(), item.fill_rows)
            for item in data_items
            if item.variable
        ]

    def add_data(self, data: Mapping, fill_rows: bool = False):
        if not is_instance(data, dict):
            data = dict(data)
        pad_to_row = max([len(self[key]) for key in data.keys()])
        for key, item in data.items():
            self[key].add_data(item, fill_rows, pad_to_row)

    def pad(self):
        if self:
            pad_to_row = max([len(item) for item in self.values()])
            [item.pad(pad_to_row) for item in self.values()]


class Variable(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fill_rows = False

    def add_data(self, data, fill_rows=False, pad_to_row=None):
        if pad_to_row is not None:
            self.pad(pad_to_row)
        self += [str(item) if isinstance(item, datetime) else item for item in data]
        self.fill_rows = fill_rows

    def pad(self, pad_to_row):
        n_additional_rows = pad_to_row - len(self)
        if n_additional_rows < 0:
            raise ValueError(
                f"Attempted to pad variable in {pad_to_row} but the variable has {len(self)} rows already."
            )
        padding_data = self[-1] if self.fill_rows and len(self) > 0 else None
        self += n_additional_rows * [padding_data]
