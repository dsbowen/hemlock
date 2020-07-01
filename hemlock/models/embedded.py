"""# Embedded data and timers"""

from ..app import db
from .bases import Data

from datetime import datetime, timedelta


class Embedded(Data):
    """
    Embedded data belong to a branch or page. Use embedded data to manually 
    input data to the dataframe; as opposed to recording data from participant 
    responses.

    Inherits from `hemlock.Data`.

    Parameters
    ----------
    parent : hemlock.Branch, hemlock.Page, or None, default=None
        The parent of this embedded data element.

    Attributes
    ----------
    branch : hemlock.Branch or None
        The branch to which the embedded data element belongs.

    page : hemlock.Page or None
        The page to which this embedded data element belongs.
    """
    id = db.Column(db.Integer, db.ForeignKey('data.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'embedded'}

    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

    def __init__(self, parent=None, **kwargs):
        from .branch import Branch
        from .page import Page
        if isinstance(parent, Branch):
            self.branch = parent
        elif isinstance(parent, Page):
            self.page = parent
        super().__init__(**kwargs)


class Timer(Embedded):
    """
    Tracks how much time a participant spends in various parts of the survey.

    Inherits from `hemlock.Embedded`.

    Attributes
    ----------
    data : float or None, default=None.
        Read only. Number of seconds for which the timer has been running.

    end_time : datetime.datetime or None, default=None
        Read only. If the timer is running, this is the current time. If the 
        timer is paused, this is the time at which the timer was last paused.

    start_time : datetime.datetime or None, default=None
        The time at which the timer was started.

    state : str, default='not started'
        `'not started'`, `'running`', or `'paused'`.

    total_time : datetime.timedelta or None, default=None
        Read only. Total time the timer has been running.

    unpause_time : datetime.datetime or None, default=None
        The time at which the timer was last unpaused.
    """
    id = db.Column(db.Integer, db.ForeignKey('embedded.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'timer'}

    _timed_page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    _data = db.Column(db.Float)
    _end_time = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    state = db.Column(db.String(16), default='not started')
    _total_time = db.Column(db.Interval)
    unpause_time = db.Column(db.DateTime)

    @property
    def data(self):
        self._set_current_time()
        return self._data

    @property
    def end_time(self):
        self._set_current_time()
        return self._end_time

    @property
    def total_time(self):
        self._set_current_time()
        return self._total_time

    def start(self):
        """
        Start the timer.

        Returns
        -------
        self : hemlock.Timer
        """
        if self.state != 'running':
            self.state = 'running'
            now = datetime.utcnow()
            if self.start_time is None:
                self.start_time = now
            self.unpause_time = now
        return self
    
    def pause(self):
        """
        Pause the timer.

        Returns
        -------
        self : hemlock.Timer
        """
        self._set_current_time()
        self.state = 'paused'
        return self

    def reset(self):
        """
        Reset all attributes to their default values.

        Returns
        -------
        self : hemlock.Timer
        """
        self._data = None
        self._end_time = None
        self.state = 'not started'
        self.start_time = None
        self._total_time = None
        self.unpause_time = None
        return self
    
    def _set_current_time(self):
        if self.state == 'running':
            self._end_time = datetime.utcnow()
            if self._total_time is None:
                self._total_time = timedelta(0)
            self._total_time += self._end_time - self.unpause_time
            self._data = self._total_time.total_seconds()