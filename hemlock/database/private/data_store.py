"""Data store database model"""

from hemlock.app.factory import db, socketio
from hemlock.database.types import DataFrameType

from datetime import datetime
from sqlalchemy_mutable import MutableDictType
import json
import pandas as pd

STATUS = ['completed', 'in_progress', 'timed_out']
DEFAULT_STATUS = {s: 0 for s in STATUS}


class DataStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    _current_status = db.Column(MutableDictType, default=DEFAULT_STATUS)
    data = db.Column(DataFrameType)
    meta = db.Column(DataFrameType)
    status_log = db.Column(DataFrameType)
    
    @property
    def current_status(self):
        """Add total Participants and time stamp to _current_status"""
        current_status = self._current_status.copy()
        current_status['total'] = sum([current_status[s] for s in STATUS])
        return current_status
    
    @classmethod
    def pascal(cls, text):
        """Convert text to pascal format"""
        text = text.replace('_', ' ')
        return ''.join([l for l in text.title() if not l.isspace()])
    
    def __init__(self):
        db.session.add(self)
        db.session.flush([self])
        self.data.filename = 'Data.csv'
        self.meta.filename = 'Metadata.csv'
        self.status_log.filename = 'StatusLog.csv'
        self.log_status()
    
    def log_status(self):
        """Append current status to the status log"""
        current_status = self.current_status
        current_status['time'] = datetime.utcnow()
        self.status_log.append(current_status)
    
    def update_status(self, part):
        """Update current status
        
        Store Participant data on completion and time out.
        """
        if part.previous_status is not None:
            self._current_status[part.previous_status] -= 1
        self._current_status[part.status] += 1
        current_status = json.dumps(self.current_status)
        socketio.emit('json', current_status, namespace='/participants-nsp')
        if part.status in ['completed', 'timed_out']:
            self.store_participant(part)
    
    def store_participant(self, part):
        """Store data for given Participant"""
        self.remove_participant(part)
        self.data.append(part.data)
        part.updated = False
        
    def remove_participant(self, part):
        """Remove data for given Participant"""
        id_var = self.data.get('ID')
        if id_var is None or part.id not in id_var:
            return
        end = start = id_var.index(part.id)
        while end < len(id_var) and id_var[end] == part.id:
            end += 1
        self.data.remove(start, end)
        
    def print_data(self, data=None):
        data = self.data if data is None else data
        df = pd.DataFrame(data)
        print(df)