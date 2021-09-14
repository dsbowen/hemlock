from datetime import datetime

from flask import request
from flask_login import UserMixin
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable.types import MutablePickleType, MutableDictJSONType

from .app import db, login_manager
from .utils.random import make_hash

HASH_LENGTH = 90
IPV4_LENGTH = 4 * 3 + 3  # 4 sets of 3 characters each plus 3 . delimiters


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    trees = db.relationship("Tree")

    @property
    def current_tree(self):
        # TODO: allow users to have multiple trees
        return self.trees[0]

    @property
    def page(self):
        return self.current_tree.page

    hash = db.Column(db.String(HASH_LENGTH))
    completed = db.Column(db.Boolean, default=False)
    failed = db.Column(db.Boolean, default=False)
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    ipv4 = db.Column(db.String(IPV4_LENGTH))
    params = db.Column(MutablePickleType)
    meta_data = db.Column(MutableDictJSONType, default={})
    cached_data = db.Column(MutableDictJSONType)

    def __init__(self):
        self.hash = make_hash(HASH_LENGTH)
        self.start_time = self.end_time = datetime.utcnow()
        self.completed = self.failed = False
        self.ipv4 = request.remote_addr
        self.meta_data = request.args

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.get_meta_data(True)}>"

    def display_navigation(self):
        return self.trees[0].display_navigation()

    def get_meta_data(self, convert_datetime_to_string=False):
        metadata = {
            "id": self.id,
            "completed": self.completed,
            "failed": self.failed,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_seconds": (self.end_time - self.start_time).total_seconds(),
        }
        if convert_datetime_to_string:
            metadata["start_time"] = str(self.start_time)
            metadata["end_time"] = str(self.end_time)
        metadata.update(self.meta_data)
        return metadata
