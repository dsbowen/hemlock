from __future__ import annotations

from typing import Any, Dict, List, Mapping, Tuple, Union

from sqlalchemy_mutable.utils import is_instance
from sqlalchemy_mutable.types import MutablePickleType, MutableListJSONType

from .app import db


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String)
    __mapper_args__ = {"polymorphic_identity": "data", "polymorphic_on": data_type}

    _page_id = db.Column(db.Integer, db.ForeignKey("page.id"))

    variable = db.Column(db.String)
    data = db.Column(MutablePickleType)
    n_rows = db.Column(db.Integer)
    fill_rows = db.Column(db.Boolean)
    index = db.Column(db.Integer)
    record_index = db.Column(db.Boolean)

    # choices = db.Column(MutableListJSONType)
    # record_choice_index = db.Column(db.Boolean, default=False)

    def __init__(
        self,
        variable: str = None,
        data: Any = None,
        n_rows: int = 1,
        fill_rows: bool = False,
        record_index: bool = False,
    ):
        self.variable = variable
        self.data = data
        self.n_rows = n_rows
        self.fill_rows = fill_rows
        self.record_index = record_index

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.variable} {self.data}>"

    def pack_data(self) -> Dict[str, List[Any]]:
        if self.variable is None:
            return {}

        data = self.data
        if not is_instance(data, list):
            data = self.n_rows * [None if data is None else data.get_object()]

        packed_data = {self.variable: data}

        if self.record_index:
            packed_data[f"{self.variable}_index"] = len(data) * [self.index]

        # if self.record_choice_index and self.choices:
        #     data.update(
        #         {
        #             "_".join([self.variable, choice.name, "index"]): index
        #             for index, choice in enumerate(self.choices)
        #             if choice.name
        #         }
        #     )

        return packed_data
