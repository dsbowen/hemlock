from __future__ import annotations

from typing import Any, Dict, List, Mapping, Tuple, Union

from sqlalchemy_mutable.types import MutablePickleType, MutableListJSONType

from .app import db


class Data(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String)
    __mapper_args__ = {"polymorphic_identity": "data", "polymorphic_on": data_type}

    _page_id = db.Column(db.Integer, db.ForeignKey("page.id"))

    variable = db.Column(db.String)
    fill_data_rows = db.Column(db.Boolean, default=False)
    data = db.Column(MutablePickleType)

    index = db.Column(db.Integer)
    record_index = db.Column(db.Boolean, default=False)

    order = None
    record_order = db.Column(db.Boolean, default=False)

    choices = db.Column(MutableListJSONType)
    record_choice_index = db.Column(db.Boolean, default=False)

    def __init__(self, variable: str = None, data: Any = None, fill_data_rows: bool = False):
        self.data = data
        self.variable = variable
        self.fill_data_rows = fill_data_rows

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.variable} {self.data}>"

    def _pack_data(self, data: Dict = None) -> Dict:
        if self.variable is None:
            return {}

        if data is None:
            data = {self.variable: self.data}
        if self.record_order:
            data[self.variable + "_order"] = self.order
        if self.record_index:
            data[self.variable + "_index"] = self.index
        if self.record_choice_index and self.choices:
            data.update(
                {
                    "_".join([self.variable, choice.name, "index"]): index
                    for index, choice in enumerate(self.choices)
                    if choice.name
                }
            )

        return data
