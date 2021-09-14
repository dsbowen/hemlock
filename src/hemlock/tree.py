import textwrap

import matplotlib.pyplot as plt
from flask import current_app, redirect, request, url_for
from sqlalchemy.ext.orderinglist import ordering_list

from ._display_navigation import display_navigation
from .app import db


class Tree(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    _user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    branch = db.relationship(
        "Page",
        backref="tree",
        order_by="Page.index",
        collection_class=ordering_list("index"),
        foreign_keys="Page._tree_id",
    )

    page = db.relationship("Page", uselist=False, foreign_keys="Page._tree_head_id")

    view_function_name = db.Column(db.String)
    request_in_progress = db.Column(db.Boolean, default=False)
    prev_request_method = db.Column(db.String(4))
    cached_page_html = db.Column(db.Text)

    def __init__(self, view_func):
        self.view_function_name = view_func.__name__
        self.branch = view_func()
        self.page = self.branch[0]

    def __repr__(self):
        initial_indent = ""
        subsequent_indent = 4 * " "

        if not self.branch:
            branch_text = ""
        else:
            branch_text = "\n".join([str(page) for page in self.branch])
            branch_text = f"\n{textwrap.indent(branch_text, subsequent_indent)}"

        return textwrap.indent(
            f"<{self.__class__.__qualname__} id: {self.id}>{branch_text}",
            initial_indent,
        )

    def display(self):
        display_navigation(self)
        plt.show()
        return self.page.display()

    def go_forward(self):
        if self.page.next_page is not None:
            self.page = self.page.next_page
            return self

        if self.page.branch:
            self.page = self.page.branch[0]
            return self

        page = self.page
        while page is page.root_branch[-1]:
            page = page.root
            if page is None:
                raise RuntimeError(
                    f"Cannot find a page to go forward to from \n{self.page}."
                )
        self.page = page.root_branch[page.index + 1]
        return self

    def go_back(self):
        if self.page.prev_page is not None:
            self.page = self.page.prev_page
            return self

        if self.page is self.page.root_branch[0]:
            if self.page.root is None:
                raise RuntimeError(
                    f"Cannot find a page to go back to from \n{self.page}"
                )
            self.page = self.page.root
            return self

        self.page = self.page.root_branch[self.page.index - 1]
        while self.page.branch:
            self.page = self.page.branch[-1]
        return self

    def process_request(self):
        # return a loading page if a request is in progress
        if self.request_in_progress:
            return current_app.settings.get("loading_page", "TODO: CREATE LOADING PAGE")

        # return the HTML for the current page if the user refreshed the page
        if request.method == self.prev_request_method == "GET":
            return self.cached_page_html

        self.request_in_progress = True
        self.prev_request_method = request.method
        db.session.commit()

        # handle GET request
        if request.method == "GET":
            page_html = self.page.get()
            self.cached_page_html = page_html
            self.request_in_progress = False
            db.session.commit()
            return page_html

        # handle POST request
        direction_from = self.page.post()
        if direction_from == "forward":
            self.go_forward()
        elif direction_from == "back":
            self.go_back()
        self.page.direction_to = direction_from

        self.request_in_progress = False
        return redirect(url_for(f"hemlock.{self.view_function_name}"))

    def test_request(self, responses=None, direction="forward"):
        self.test_post(responses, direction)
        self.test_get()
        return self

    def test_get(self):
        with current_app.test_request_context():
            self.process_request()
        return self

    def test_post(self, responses=None, direction="forward"):
        data = {}
        if isinstance(responses, dict):
            data = {key.hash: item for key, item in responses.items()}
        elif isinstance(responses, (list, tuple)):
            data = {
                question.hash: item
                for question, item in zip(self.page.questions, responses)
            }
        data["direction"] = direction

        with current_app.test_request_context(method="POST", data=data):
            self.process_request()
        return self
