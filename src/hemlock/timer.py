"""Timer.
"""
from __future__ import annotations

from datetime import datetime

from sqlalchemy.ext.hybrid import hybrid_property

from .app import db
from .data import Data


class Timer(Data):
    """Timer.

    Subclasses :class:`hemlock.data.Data`.

    Attributes:
        is_running (bool): Indicates that the timer is running.
        start_time (datetime): The most recent time the timer was started.
        total_seconds (float): The total number of seconds the timer has been running.

    Examples:

        .. code-block::

            >>> import time
            >>> from hemlock.timer import Timer
            >>> timer = Timer("my_timer_variable")
            >>> timer
            <Timer my_timer_variable paused 0 seconds>
            >>> timer.start()
            >>> time.sleep(1)
            >>> timer
            <Timer my_timer_variable running 1.015078 seconds>
            >>> timer.pause()
            >>> timer
            <Timer my_timer_variable paused 5.425622 seconds>
            >>> timer.pack_data()
            {'my_timer_variable': [5.425622]}
    """

    id = db.Column(db.Integer, db.ForeignKey("data.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "timer"}

    _page_timer_id = db.Column(db.Integer, db.ForeignKey("page.id"))

    is_running = db.Column(db.Boolean)
    start_time = db.Column(db.DateTime)

    @hybrid_property
    def total_seconds(self) -> float:
        """Get the total number of seconds the timer has been running.

        Returns:
            float: Total seconds.
        """
        if self.is_running:
            return self.data + (datetime.utcnow() - self.start_time).total_seconds()
        return self.data

    @total_seconds.setter  # type: ignore
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
        """Start the timer."""
        if not self.is_running:
            self.is_running = True
            self.start_time = datetime.utcnow()

    def pause(self):
        """Pause the timer."""
        if self.is_running:
            self.data += (datetime.utcnow() - self.start_time).total_seconds()
            self.is_running = False
