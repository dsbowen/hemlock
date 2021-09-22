"""Timer.
"""
from __future__ import annotations

from datetime import datetime

from .app import db
from .data import Data


class Timer(Data):
    """Timer.

    Subclasses :class:`hemlock.Data`.

    Attributes:
        is_running (bool): Indicates that the timer is running.
        start_time (datetime): The most recent time the timer was started.
        total_seconds (float): The total number of seconds the timer has been running.
    """
    id = db.Column(db.Integer, db.ForeignKey("data.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "timer"}

    _page_timer_id = db.Column(db.Integer, db.ForeignKey("page.id"))

    is_running = db.Column(db.Boolean)
    start_time = db.Column(db.DateTime)

    @property
    def total_seconds(self):
        if self.is_running:
            return self.data + (datetime.utcnow() - self.start_time).total_seconds()
        return self.data

    @total_seconds.setter
    def total_seconds(self, total_seconds):
        self.data = total_seconds

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_running = False
        self.total_seconds = 0

    def __repr__(self):
        running = "running" if self.is_running else "paused"
        return f"<{self.__class__.__qualname__} {self.variable} {running} {self.total_seconds} seconds>"

    def start(self):
        """Start the timer.
        """
        if not self.is_running:
            self.is_running = True
            self.start_time = datetime.utcnow()

    def pause(self):
        """Pause the timer.
        """
        if self.is_running:
            self.total_seconds += (datetime.utcnow() - self.start_time).total_seconds()
        self.is_running = False
