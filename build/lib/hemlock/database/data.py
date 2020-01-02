"""Data elements base, Embedded data models, and Timer models

The `Data` model is a base for data elements (`Embedded` data and 
`Question`s). Data elements contribute data to the dataset, by 'packing' 
their data and returning it to a `Participant`, who in turn sends it to the 
`DataStore`.

Unlike `Question`s, `Embedded` data do not derive their data directly from 
participant input. Rather, the data are set by a programmer. `Embedded` 
data are stored in a `Branch` or `Page` separately from questions.

`Timer`s are a type of `Embedded` data. Each `Page` has a `Timer` by 
default. To record a `Timer`'s data, set its variable (e.g. 
timer.var='MyTimingVariable').
"""

from hemlock.app import db
from hemlock.database.bases import Base, HTMLMixin

from sqlalchemy_mutable import MutableType

from datetime import datetime


class Data(Base, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data_type = db.Column(db.String)
    __mapper_args__ = {
        'polymorphic_identity': 'data',
        'polymorphic_on': data_type
    }

    _page_id = db.Column(db.Integer, db.ForeignKey('page.id'))
    _branch_id = db.Column(db.Integer, db.ForeignKey('branch.id'))

    all_rows = db.Column(db.Boolean)
    data = db.Column(MutableType)
    index = db.Column(db.Integer)
    order = db.Column(db.Integer)
    var = db.Column(db.Text)

    def _pack_data(self, data=None):
        """Pack data for storing in DataStore
        
        Note: `var`Index is the index of the object; its order within its
        Branch, Page, or Question. `var`Order is the order of the Question
        relative to other Questions with the same variable.
        
        The optional `data` argument is prepacked data from the element.
        """
        if self.var is None:
            return {}
        data = {self.var: self.data} if data is None else data
        if not self.all_rows:
            data[self.var+'Order'] = self.order
        if self.index is not None:
            data[self.var+'Index'] = self.index
        if hasattr(self, 'choices'):
            for c in self.choices:
                if c.name is not None:
                    data[self.var + c.name + 'Index'] = c.index
        return data


class Embedded(Data):
    id = db.Column(db.Integer, db.ForeignKey('data.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'embedded'}

    @Data.init('Embedded')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        return {'page': page, **kwargs}


class Timer(Embedded):
    id = db.Column(db.Integer, db.ForeignKey('embedded.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'timer'}

    _timed_page_id = db.Column(db.Integer, db.ForeignKey('page.id'))

    state = db.Column(db.String(16), default='not_started')
    start_time = db.Column(db.DateTime)
    unpause_time = db.Column(db.DateTime)
    _end_time = db.Column(db.DateTime)
    _total_time = db.Column(db.Interval)
    _data = db.Column(db.Float)

    @Base.init('Timer')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        return {'page': page, **kwargs}

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

    def start(self):
        now = datetime.utcnow()
        if self.start_time is None:
            self.start_time = now
        self.unpause_time = now
        self.state = 'running'
    
    def pause(self):
        self._set_current_time()
        self.state = 'paused'
    
    def _set_current_time(self):
        if self.state == 'running':
            self._end_time = datetime.utcnow()
            self._total_time = self._end_time - self.unpause_time
            self._data = self._total_time.total_seconds()