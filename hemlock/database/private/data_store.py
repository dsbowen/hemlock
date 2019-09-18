"""Data store database model"""

from hemlock.app.factory import db
from hemlock.database.types import DataFrameType

from datetime import datetime
from flask import current_app
from sqlalchemy_mutable import MutableDictType
import pandas as pd


class DataStore(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(DataFrameType, default={})
    meta = db.Column(DataFrameType, default={})
    status_log = db.Column(DataFrameType, default={})
    
    @classmethod
    def pascal(cls, text):
        """Convert text to pascal format"""
        text = text.replace('_', ' ')
        return ''.join([l for l in text.title() if not l.isspace()])
    
    def __init__(self):
        db.session.add(self)
        db.session.flush([self])
        self.log_status()
    
    def log_status(self):
        """Add time stamp and update status log"""
        current_status = current_app.current_status.copy()
        current_status['time'] = datetime.utcnow()
        self.status_log.append(current_status)
    
    def store_participant(self, part):
        """Store data for given Participant"""
        self.remove_participant(part)
        self.data.append(part.data)
        
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