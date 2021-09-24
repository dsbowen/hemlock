from __future__ import annotations

import functools
from datetime import datetime
from typing import Mapping, Optional, Union

import pandas as pd
from flask import current_app, request
from flask_login import UserMixin, current_user, login_required
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates
from sqlalchemy.types import JSON
from sqlalchemy_mutable.types import MutablePickleType, MutableDictJSONType

from ._data_frame import DataFrame
from .app import bp, db, login_manager
from .tree import Tree
from .utils.random import make_hash

HASH_LENGTH = 90


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    _seed_funcs = {}
    default_url_rule = None

    id = db.Column(db.Integer, primary_key=True)

    trees = db.relationship(
        "Tree", order_by="Tree.index", collection_class=ordering_list("index")
    )

    @classmethod
    def route(cls, url_rule, default=False):
        def register(seed_func):
            @bp.route(url_rule, methods=["GET", "POST"])
            @login_required
            @functools.wraps(seed_func)
            def view_function():
                return current_user.process_request(url_rule)

            index = 0
            if cls._seed_funcs:
                index = list(cls._seed_funcs.values())[-1][0] + 1
            cls._seed_funcs[url_rule] = index, seed_func

            return seed_func

        if default or cls.default_url_rule is None:
            cls.default_url_rule = url_rule

        return register

    @classmethod
    def make_test_user(cls, seed_func=None, url_rule="/test"):
        user = cls()
        db.session.add(user)
        db.session.commit()

        if seed_func is not None:
            index = 0
            if user._seed_funcs:
                index = list(user._seed_funcs.values())[-1][0] + 1
            user._seed_funcs = user._seed_funcs.copy()
            user._seed_funcs[url_rule] = index, seed_func
            user.default_url_rule = url_rule
            user.trees.append(Tree(seed_func, url_rule))

        return user

    hash = db.Column(db.String(HASH_LENGTH))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    params = db.Column(MutablePickleType)
    meta_data = db.Column(MutableDictJSONType, default={})
    _cached_data = db.Column(JSON)

    _completed = db.Column(db.Boolean)

    @property
    def completed(self) -> Optional[bool]:
        return self._completed

    @completed.setter
    def completed(self, completed: bool):
        self._completed = completed
        if completed:
            self._cached_data = self.get_data(to_pandas=False, use_cached_data=False)

    _failed = db.Column(db.Boolean)

    @property
    def failed(self) -> Optional[bool]:
        return self._failed

    @failed.setter
    def failed(self, failed: bool):
        self._failed = failed
        if failed:
            self._cached_data = self.get_data(to_pandas=False, use_cached_data=False)

    def __init__(self, meta_data: Mapping = None):
        self.hash = make_hash(HASH_LENGTH)
        self.start_time = self.end_time = datetime.utcnow()
        self.completed = self.failed = False
        self.meta_data = meta_data or {}
        # self.ipv4 = request.remote_addr
        # self.meta_data = request.args
        self.trees = [Tree(func) for _, func in self._seed_funcs.values()]

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.get_meta_data(True)}>"

    def get_tree(self, url_rule=None) -> Tree:
        # get the index of the requested tree
        index = self._seed_funcs[url_rule or self.default_url_rule][0]
        return self.trees[index]

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

    def get_data(
        self, to_pandas: bool = True, use_cached_data: bool = True
    ) -> Union[pd.DataFrame, DataFrame]:
        if use_cached_data and self._cached_data is not None:
            df = self._cached_data
        else:
            meta_data = self.get_meta_data(convert_datetime_to_string=True)
            meta_data = {key: [item] for key, item in meta_data.items()}
            df = DataFrame(meta_data, fill_rows=True)
            [df.add_branch(tree.branch) for tree in self.trees]
            df.pad()

        return pd.DataFrame(df) if to_pandas else df

    @staticmethod
    def get_all_data(
        to_pandas: bool = True, cached_data_only: bool = True
    ) -> Union[pd.DataFrame, DataFrame]:
        if cached_data_only:
            users = User.query.filter(User._cached_data != None).all()
        else:
            users = User.query.all()

        df = DataFrame()
        [df.add_data(user.get_data(to_pandas=False)) for user in users]

        return pd.DataFrame(df) if to_pandas else df

    def process_request(self, url_rule):
        if request.method == "POST":
            self.end_time = datetime.utcnow()

        current_tree = self.get_tree(url_rule)
        if current_tree.page.is_last_page and [
            tree.page.is_last_page for tree in self.trees
        ]:
            self.completed = True

        return current_tree.process_request()

    def test_request(self, responses=None, direction="forward", url_rule=None):
        self.test_post(responses, direction, url_rule)
        return self.test_get(url_rule)

    def test_get(self, url_rule=None):
        url_rule = url_rule or self.default_url_rule
        with current_app.test_request_context():
            self.process_request(url_rule)
        return self.get_tree(url_rule)

    def test_post(self, responses=None, direction="forward", url_rule=None):
        url_rule = url_rule or self.default_url_rule
        tree = self.get_tree(url_rule)

        data = {
            question.hash: question.get_default() for question in tree.page.questions
        }
        if isinstance(responses, dict):
            data.update({key.hash: item for key, item in responses.items()})
        elif isinstance(responses, (list, tuple)):
            data = {
                question.hash: item
                for question, item in zip(tree.page.questions, responses)
            }
        data["direction"] = direction

        with current_app.test_request_context(method="POST", data=data):
            self.process_request(url_rule)
        return tree
