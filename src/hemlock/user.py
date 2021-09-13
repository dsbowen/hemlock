from datetime import datetime

from flask import request
from flask_login import UserMixin, login_user
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy_mutable.types import MutablePickleType, MutableDictJSONType

from ._display_navigation import display_navigation
from .app import db
from .utils.random import make_hash

HASH_LENGTH = 90
IPV4_LENGTH = 4 * 3 + 3  # 4 sets of 3 characters each plus 3 . delimiters


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)

    page = db.relationship(
        "Page",
        uselist=False,
        foreign_keys="Page._user_head_id"
    )

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
        return display_navigation(self)

    def get_meta_data(self, convert_datetime_to_string=False):
        metadata = {
            "id": self.id,
            "completed": self.completed,
            "failed": self.failed,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_seconds": (self.end_time - self.start_time).total_seconds()
        }
        if convert_datetime_to_string:
            metadata["start_time"] = str(self.start_time)
            metadata["end_time"] = str(self.end_time)
        metadata.update(self.meta_data)
        return metadata

    def go_forward(self):
        def find_next_page_in_next_branch(next_branch):
            while next_branch is not None:
                if next_branch.pages:
                    self.page = next_branch.pages[0]
                    return True
                
                next_branch = next_branch.next_branch

            return False

        # if the next page is explicitly specified, go there
        if self.page.next_page is not None:
            self.page = self.page.next_page
            return self

        # look for the next page in the page's next branch
        if find_next_page_in_next_branch(self.page.next_branch):
            return self

        # look for the next page in the page's current branch
        if self.page is not self.page.branch.pages[-1]:
            self.page = self.page.branch.pages[self.page.index + 1]
            return self

        # look for the next page in the current branch's next branch
        if find_next_page_in_next_branch(self.page.branch.next_branch):
            return self

        # look for next page in a previous branch
        branch = self.page.branch
        while branch is not None:
            prev_page = branch.prev_page
            if prev_page is not None:
                branch = prev_page.branch
                if prev_page is not branch.pages[-1]:
                    self.page = branch.pages[prev_page.index + 1]
                    return self
                if find_next_page_in_next_branch(branch.next_branch):
                    return self
            else:
                branch = branch.prev_branch

        raise RuntimeError(f"There are no pages to navigate forward to from \n{self.page}")

    def go_back(self):
        def find_last_page_in_subtree(page):
            # get the last branch in the subtree that has pages
            next_branch = page.next_branch
            last_branch_with_pages = None
            while next_branch is not None:
                if next_branch.pages:
                    last_branch_with_pages = next_branch
                next_branch = next_branch.next_branch

            if last_branch_with_pages is None:
                self.page = page
                return self

            return find_last_page_in_subtree(last_branch_with_pages.pages[-1])

        # if the previous page is explicitly specified, go there
        if self.page.prev_page is not None:
            self.page = self.page.prev_page
            return self

        # look for the previous page in the subtree associated with the previous page
        # on the same branch
        if self.page is not self.page.branch.pages[0]:
            prev_page = self.page.branch.pages[self.page.index - 1]
            return find_last_page_in_subtree(prev_page)

        # look for the previous page in the subtree of a previous branch
        branch = self.page.branch
        while branch is not None:
            prev_page = branch.prev_page
            if prev_page is not None:
                self.page = prev_page
                return self

            branch = branch.prev_branch
            if branch is not None and branch.pages:
                return find_last_page_in_subtree(branch.pages[-1])

        raise RuntimeError(f"There are no pages to navigate back to from \n{self.page}")
