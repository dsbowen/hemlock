"""Participant metadata database model"""

from hemlock.app.factory import db
from hemlock.database.types import DataFrameType


class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(DataFrameType, default={})
    
    def __init__(self):
        db.session.add(self)
        db.session.flush([self])