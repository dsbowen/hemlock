"""Embedded and Timer data element polymorphs"""

from hemlock.database.data.utils import *

from datetime import datetime


class Embedded(Data):
    id = db.Column(db.Integer, db.ForeignKey('data.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'embedded'}

    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))
    
    @Data.init('Embedded')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        return {'page': page, **kwargs}


class Timer(Embedded):
    id = db.Column(db.Integer, db.ForeignKey('embedded.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'timer'}

    state = db.Column(db.String(16), default='not_started')
    start_time = db.Column(db.DateTime)
    unpause_time = db.Column(db.DateTime)
    _end_time = db.Column(db.DateTime)
    _total_time = db.Column(db.Interval)
    _data = db.Column(db.Float)

    @property
    def end_time(self):
        self._set_current_time()
        return self._end_time

    @end_time.setter
    def end_time(self, val):
        self._end_time = val

    @property
    def total_time(self):
        self._set_current_time()
        return self._total_time

    @total_time.setter
    def total_time(self, val):
        self._total_time = val

    @property
    def data(self):
        self._set_current_time()
        return self._data

    @data.setter
    def data(self, val):
        self._data = val

    def _set_current_time(self):
        if self.state == 'running':
            self._end_time = datetime.utcnow()
            self._total_time = self._end_time - self.unpause_time
            self._data = self._total_time.total_seconds()

    @Embedded.init('Timer')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        return {'page': page, **kwargs}

    def start(self):
        now = datetime.utcnow()
        if self.start_time is None:
            self.start_time = now
        self.unpause_time = now
        self.state = 'running'
    
    def pause(self):
        self._set_current_time()
        self.state = 'paused'