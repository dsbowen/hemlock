"""Status logger database model

Logs the app's status tracker at regular intervals. This allows researchers to
track the traffic to their survey over time.
"""

from hemlock.app.factory import db

from datetime import datetime
from flask import current_app
from sqlalchemy_mutable import MutableListType


class StatusLogger(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    log = db.Column(MutableListType, default=[])
    
    def __init__(self):
        db.session.add(self)
        db.session.flush([self])
        self.update_log()
    
    def update_log(self):
        """Add timestamp and update the status log"""
        status_tracker = current_app.status_tracker.copy()
        status_tracker['time'] = datetime.utcnow()
        self.log.append(status_tracker)