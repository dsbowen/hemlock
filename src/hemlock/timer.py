from __future__ import annotations

from datetime import datetime
from typing import Dict

from .app import db
from .data import Data


class Timer(Data):
    id = db.Column(db.Integer, db.ForeignKey("data.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "timer"}

    _page_timer_id = db.Column(db.Integer, db.ForeignKey("page.id"))

    is_running = db.Column(db.Boolean)
    start_time = db.Column(db.DateTime)
    _total_seconds = db.Column(db.Float)

    @property
    def total_seconds(self):
        if self.is_running:
            return self._total_seconds + (datetime.utcnow() - self.start_time).total_seconds()
        return self._total_seconds

    @total_seconds.setter
    def total_seconds(self, total_seconds):
        self._total_seconds = total_seconds

    def __init__(self, *args, **kwargs):
        self.is_running = False
        self.total_seconds = 0
        super().__init__(*args, **kwargs)

    def __repr__(self):
        running = "running" if self.is_running else "paused"
        return f"<{self.__class__.__qualname__} {self.variable} {running} {self.total_seconds} seconds>"

    def start(self):
        if not self.is_running:
            self.is_running = True
            self.start_time = datetime.utcnow()
        return self

    def pause(self):
        if self.is_running:
            self.total_seconds += (datetime.utcnow() - self.start_time).total_seconds()
        self.is_running = False
        return self

    def _pack_data(self, data: Dict = None) -> Dict:
        return super()._pack_data(data or {self.variable: self.total_seconds})
