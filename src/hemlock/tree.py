"""Tree.
"""
from __future__ import annotations

import textwrap
from typing import TYPE_CHECKING, Any, Callable, List, Union, TypeVar

import matplotlib.pyplot as plt
from IPython import display
from flask import redirect, render_template, request, url_for
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.orderinglist import ordering_list
from werkzeug.wrappers.response import Response

from ._display_navigation import display_navigation
from .app import db, static_pages
from .page import Page

if TYPE_CHECKING:
    from .page import Page

TreeType = TypeVar("TreeType", bound="Tree")


class Tree(db.Model):
    """Tree.

    The tree contains a main branch of pages. (Pages may also have their own branches).
    Trees control which page the user navigates to next in response to a request.

    Args:
        seed_func (Callable[[], List[Page]]): The "seed function" initializes the
            tree's branch.

    Attributes:
        user (User): The user to which this tree belongs.
        index (int): Position of this tree relative to other trees belonging to the
            same user.
        branch (List[Page]): A list of pages returned by the seed function.
        page (Page): The page this tree is currently on.
        request_in_progress (bool): Indicates that this tree is currently processing
            its user's request.
        prev_request_method (str): The request method of the user's previous request.
            Either "GET" or "POST".
        cached_page_html (str): Cached HTML from the user's last GET request.
    """

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

    _seed_func_name = db.Column(db.String)
    _url_rule = db.Column(db.String)
    request_in_progress = db.Column(db.Boolean, default=False)
    prev_request_method = db.Column(db.String(4))
    cached_page_html = db.Column(db.Text)
    index = db.Column(db.Integer)

    @hybrid_property
    def url_rule(self) -> str:
        """Get the URL rule associated with requests to this tree.

        Returns:
            str: URL rule.
        """
        if self._url_rule is not None:
            return self._url_rule

        return url_for(f"hemlock.{self._seed_func_name}")

    def __init__(
        self,
        seed_func: Callable[[], Union[Page, List[Page]]],
        url_rule: str = None,
    ):
        self._seed_func_name = seed_func.__name__
        self._url_rule = url_rule
        branch = seed_func()
        self.branch = branch if isinstance(branch, list) else [branch]
        self.page = self.branch[0]

    def __repr__(self):
        initial_indent = ""
        subsequent_indent = 4 * " "

        branch_text = "\n".join([str(page) for page in self.branch])
        branch_text = f"\n{textwrap.indent(branch_text, subsequent_indent)}"

        return textwrap.indent(
            f"<{self.__class__.__qualname__} id: {self.id}>{branch_text}",
            initial_indent,
        )

    def display(
        self,
        ax: plt.axes._subplots.AxesSubplot = None,
        node_size: int = 1200,
        **subplots_kwargs: Any,
    ) -> None:
        """Display the tree's navigation graph and its current page.

        Args:
            ax (plt.axes._subplots.AxesSubplot, optional): Plot on which to write the
                tree's navigation graph. Defaults to None.
            node_size (int, optional): Size of nodes in the navigation graph. Defaults
                to 1200.
            **subplots_kwargs (Any): Keyword arguments for ``plt.subplots``.
        """
        ax = display_navigation(self, ax, node_size, **subplots_kwargs)
        plt.show()
        display.display(self.page.display())

    def go_forward(self: TreeType) -> TreeType:
        """Go forward from the current page.

        Raises:
            RuntimeError: Users cannot go forward from the last page.

        Returns:
            TreeType: self.
        """
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

    def go_back(self: TreeType) -> TreeType:
        """Go back from the current page.

        Raises:
            RuntimeError: Users cannot go back from the first page.

        Returns:
            TreeType: self.
        """
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

    def process_request(self) -> Union[str, Response]:
        """Process a user's request and navigate in the appropriate direction.

        Returns:
            Union[str, Response]: HTML of the next page.
        """
        # return a loading page if a request is in progress
        if self.request_in_progress:
            loading_page_key = "loading_page"
            if loading_page_key not in static_pages:
                static_pages[loading_page_key] = render_template(
                    "hemlock/utils/loading_page.html", page=Page()
                )

            return static_pages[loading_page_key]

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
            return page_html

        # handle POST request
        direction_from = self.page.post()
        if direction_from == "forward":
            self.go_forward()
        elif direction_from == "back":
            self.go_back()
        self.page.direction_to = direction_from

        self.request_in_progress = False
        return redirect(self.url_rule)
