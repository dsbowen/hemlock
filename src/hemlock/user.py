import functools
from datetime import date, datetime

from flask import current_app, request
from flask_login import UserMixin, current_user, login_required
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable.types import MutablePickleType, MutableDictJSONType

from .app import bp, db, login_manager
from .tree import Tree
from .utils.random import make_hash

HASH_LENGTH = 90
IPV4_LENGTH = 4 * 3 + 3  # 4 sets of 3 characters each plus 3 . delimiters


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
        with current_app.test_request_context():
            user = cls()

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

    def process_request(self, url_rule):
        # TODO: cache data when user has completed or failed the survey
        self.end_time = datetime.utcnow()
        return self.get_tree(url_rule).process_request()

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
