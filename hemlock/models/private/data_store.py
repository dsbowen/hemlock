"""Data store"""

from ...app import db, socketio
from .data_frame import DataFrameType

import json
import pandas as pd
from sqlalchemy_mutable import MutableDictJSONType

from datetime import datetime

STATUS = ['Completed', 'InProgress', 'TimedOut']
DEFAULT_STATUS = {s: 0 for s in STATUS}


class DataStore(db.Model):
    """
    Each app has a unique data store.

    It contains two dataframes:

    1. `data`. The primary dataframe
    2. `meta`. Participant metadata, used to detect screenouts and duplicates.
    """
    id = db.Column(db.Integer, primary_key=True)
    _current_status = db.Column(MutableDictJSONType, default=DEFAULT_STATUS)
    data = db.Column(DataFrameType, default={})
    meta = db.Column(DataFrameType, default={})
    parts_stored = db.relationship('Participant')
    
    @property
    def current_status(self):
        """Add total Participants and time stamp to _current_status"""
        current_status = self._current_status.copy()
        current_status['Total'] = sum([current_status[s] for s in STATUS])
        return current_status
    
    def __init__(self):
        self.data, self.meta = {}, {}
        self.data.filename = 'data.csv'
        self.meta.filename = 'metadata.csv'
    
    def update_status(self, part):
        """Update current status
        
        Store Participant data on completion and time out.
        """
        if part._previous_status is not None:
            count = self._current_status[part._previous_status]
            self._current_status[part._previous_status] = max(count-1, 0)
        self._current_status[part.status] += 1
        current_status = json.dumps(self.current_status)
        socketio.emit('json', current_status, namespace='/participants-nsp')
        if part.status in ['Completed', 'TimedOut']:
            self.store_participant(part)
    
    def store_participant(self, part):
        """Store data for given Participant"""
        self.remove_participant(part)
        self.data.append(part.get_data())
        self.parts_stored.append(part)
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
        
    def to_pandas(self, dataframe='data'):
        """
        Parameters
        ----------
        dataframe : str
            Name of the dataframe to convert to pandas.

        Returns
        -------
        df : pandas.DataFrame
            Dataframe representation of the participant data.
        """
        return pd.DataFrame(getattr(self, dataframe) or {})