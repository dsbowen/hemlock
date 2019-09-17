"""Participant metadata database model"""

from hemlock.app.factory import db

from sqlalchemy_mutable import MutableDictType

class Metadata(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    meta = db.Column(MutableDictType, default={})
    
    def __init__(self):
        db.session.add(self)
        db.session.flush([self])
    
    @property
    def num_participants(self):
        if not self.meta.values():
            return 0
        return len(list(self.meta.values())[0])
    
    def add(self, meta):
        """Add Participant metadata""" 
        part_only_keys = set(meta.keys()) - set(self.meta.keys())
        self_only_keys = set(self.meta.keys()) - set(meta.keys())
        for key in part_only_keys:
            self.meta[key] = [None]*self.num_participants
        [self.meta[key].append(meta[key]) for key in meta.keys()]
        [self.meta[key].append(None) for key in self_only_keys]