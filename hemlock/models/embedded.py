"""# Embedded data and timers"""

from ..app import db
from .bases import Data

from datetime import datetime, timedelta


class Embedded(Data):
    """
    Embedded data belong to a branch or page. Use embedded data to manually 
    input data to the dataframe; as opposed to recording data from participant 
    responses.

    Polymorphic with [`hemlock.models.Data`](bases.md).

    Parameters
    ----------
    var : str or None, default=None
        Variable name associated with this data element. If `None`, the data 
        will not be recorded.

    data : sqlalchemy_mutable.MutableType
        Data this element contributes to the dataframe.

    data_rows : int, default=1
        Number of rows this data element contributes to the dataframe for its 
        participant. If negative, this data element will 'fill in' any emtpy
        rows at the end of the dataframe with its most recent value.

    Relationships
    -------------
    participant : hemlock.Participant or None
        The participant to whom this data element belongs.

    branch : hemlock.Branch or None
        The branch to which the embedded data element belongs.

    page : hemlock.Page or None
        The page to which this embedded data element belongs.

    Examples
    --------
    ```python
    from hemlock import Branch, Embedded, Page, Participant, push_app_context

    def start():
    \    return Branch(Page())

    app = push_app_context()

    part = Participant.gen_test_participant(start)
    part.embedded = [Embedded('Name', 'Socrates', data_rows=-1)]
    part.get_data()
    ```

    Out:

    ```
    {'ID': [1],
    'EndTime': [datetime.datetime(2020, 7, 4, 17, 57, 23, 854272)],
    'StartTime': [datetime.datetime(2020, 7, 4, 17, 57, 23, 854272)],
    'Status': ['InProgress'],
    'Name': ['Socrates'],
    'NameOrder': [0],
    'NameIndex': [0]}
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('data.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'embedded'}

    _part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

    def __init__(self, var=None, data=None, data_rows=1, **kwargs):
        self.var = var
        self.data = data
        self.data_rows = data_rows
        super().__init__(**kwargs)


class Timer(Embedded):
    """
    Tracks how much time a participant spends in various parts of the survey.

    Inherits from `hemlock.Embedded`.

    Attributes
    ----------
    data : float or None
        Read only. Number of seconds for which the timer has been running.

    end_time : datetime.datetime or None
        Read only. If the timer is running, this is the current time. If the 
        timer is paused, this is the time at which the timer was last paused.

    start_time : datetime.datetime or None
        The time at which the timer was started.

    state : str
        `'not started'`, `'running`', or `'paused'`.

    total_time : datetime.timedelta or None
        Read only. Total time the timer has been running.

    Examples
    --------
    ```python
    from hemlock import Timer, push_app_context

    import time

    app = push_app_context()

    timer = Timer()
    print(timer.state)
    timer.start()
    print(timer.state)
    time.sleep(1)
    print(timer.data)
    timer.pause()
    print(timer.state)
    time.sleep(1)
    print(timer.data)
    ```

    Out:

    ```
    not started
    running
    1.002405
    paused
    1.002983
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('embedded.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'timer'}

    _timed_page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    _data = db.Column(db.Float)
    _end_time = db.Column(db.DateTime)
    start_time = db.Column(db.DateTime)
    state = db.Column(db.String(16), default='not started')
    _total_time = db.Column(db.Interval)

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

    def __init__(self, var=None, data_rows=1, **kwargs):
        self.var = var
        self.data_rows = data_rows
        [setattr(self, key, val) for key, val in kwargs]

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
            self._end_time = now
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
        return self
    
    def _set_current_time(self):
        if self.state == 'running':
            now = datetime.utcnow()
            if self._total_time is None:
                self._total_time = timedelta(0)
            self._total_time += now - self._end_time
            self._end_time = now
            self._data = self._total_time.total_seconds()