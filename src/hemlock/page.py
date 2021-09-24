from __future__ import annotations

import copy
import os
import textwrap
from random import sample
from typing import Any, Callable, List, Mapping, Union

from IPython import display
from flask import render_template, request
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates
from sqlalchemy_mutable.html import HTMLSettingType
from sqlalchemy_mutable.types import HTMLSettingsType, MutablePickleType
from sqlalchemy_mutable.utils import is_instance

from ._custom_types import MutableListPickleType
from .app import db
from .data import Data
from .timer import Timer
from .utils.random import make_hash

HASH_LENGTH = 10
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    defaults = dict(
        navbar=None,
        error=None,
        back=False,
        forward=True,
        template="hemlock/page.html",
        compile=[],
        submit=[],
        navigate=None,
        debug=[],
        rerun_compile_functions=False,
        params=None,
        html_settings={
            "css": open(os.path.join(DIR_PATH, "_page_css.html"), "r")
            .read()
            .splitlines(),
            "js": open(os.path.join(DIR_PATH, "_page_js.html"), "r")
            .read()
            .splitlines(),
            "div": {"class": ["container", "vh-100", "d-flex", "align-items-center"]},
            "back-button": {
                "id": "back-button",
                "class": ["btn", "btn-primary"],
                "name": "direction",
                "value": "back",
                "type": "submit",
                "style": {"float": "left"},
            },
            "forward-button": {
                "id": "forward-button",
                "class": ["btn", "btn-primary"],
                "name": "direction",
                "value": "forward",
                "type": "submit",
                "style": {"float": "right"},
            },
        },
    )

    _tree_id = db.Column(db.Integer, db.ForeignKey("tree.id"))
    _tree_head_id = db.Column(db.Integer, db.ForeignKey("tree.id"))

    _branch_id = db.Column(db.Integer, db.ForeignKey("page.id"))
    branch = db.relationship(
        "Page",
        backref=db.backref("root", remote_side=[id]),
        order_by="Page.index",
        collection_class=ordering_list("index"),
        foreign_keys=_branch_id,
    )

    _prev_page_id = db.Column(db.Integer, db.ForeignKey("page.id"))
    prev_page = db.relationship("Page", foreign_keys=_prev_page_id, remote_side=[id])

    _next_page_id = db.Column(db.Integer, db.ForeignKey("page.id"))
    next_page = db.relationship("Page", foreign_keys=_next_page_id, remote_side=[id])

    data = db.relationship(
        "Data",
        order_by="Data.index",
        collection_class=ordering_list("index"),
        foreign_keys="Data._page_id",
    )

    timer = db.relationship("Timer", uselist=False, foreign_keys="Timer._page_timer_id")

    questions = db.relationship(
        "Question",
        backref="page",
        order_by="Question.index",
        collection_class=ordering_list("index"),
        foreign_keys="Question._page_question_id",
    )

    # HTML attributes
    hash = db.Column(db.String(HASH_LENGTH))
    navbar = db.Column(db.Text)
    back = db.Column(db.String)
    forward = db.Column(db.String)
    template = db.Column(db.String)
    html_settings = db.Column(HTMLSettingsType)

    @validates("back", "forward")
    def _validate_direction(
        self, key: str, value: Union[str, bool, None]
    ) -> Union[str, None]:
        if not value:
            return None

        if value is True:
            return ">>" if key == "forward" else "<<"

        return value

    # Function attributes
    compile = db.Column(MutableListPickleType)
    submit = db.Column(MutableListPickleType)
    navigate = db.Column(MutablePickleType)
    debug = db.Column(MutableListPickleType)

    # Additional attributes
    params = db.Column(MutablePickleType)
    direction_from = db.Column(db.String(8))
    direction_to = db.Column(db.String(8))
    index = db.Column(db.Integer)
    terminal = db.Column(db.Boolean, default=False)
    rerun_compile_functions = db.Column(db.Boolean)

    def __init__(
        self,
        *questions: questions.base.Question,
        timer: Union[str, Timer] = None,
        data: List[Data] = None,
        navbar=None,
        back: Union[bool, str] = None,
        prev_page: Page = None,
        forward: Union[bool, str] = None,
        next_page: Page = None,
        template: str = "hemlock/page.html",
        compile: Union[Callable, List[Callable]] = None,
        rerun_compile_functions: bool = None,
        submit: Union[Callable, List[Callable]] = None,
        navigate: Callable = None,
        debug: Union[Callable, List[Callable]] = None,
        terminal: bool = False,
        params: Any = None,
        extra_html_settings: Mapping[str, HTMLSettingType] = None,
    ):
        def set_attribute(name, value, copy_default=False):
            if value is None:
                value = self.defaults[name]
                if copy_default:
                    value = copy.deepcopy(value)

            setattr(self, name, value)

        self.hash = make_hash(HASH_LENGTH)

        self.questions = list(questions)
        self.timer = Timer(variable=timer) if is_instance(timer, str) else Timer()
        self.data = [] if data is None else data

        set_attribute("navbar", navbar, True)
        set_attribute("back", back)
        self.prev_page = prev_page
        set_attribute("forward", forward)
        self.next_page = next_page
        set_attribute("template", template)

        set_attribute("compile", compile, True)
        set_attribute("rerun_compile_functions", rerun_compile_functions)
        set_attribute("submit", submit, True)
        set_attribute("navigate", navigate, True)
        set_attribute("debug", debug, True)

        self.terminal = terminal
        set_attribute("params", params, True)

        self.html_settings = copy.deepcopy(self.defaults["html_settings"])
        if extra_html_settings is not None:
            self.html_settings.update_settings(extra_html_settings)

    def __repr__(self):
        initial_indent = ""
        subsequent_indent = 4 * " "

        if not self.questions:
            question_text = ""
        else:
            question_text = "\n".join([str(question) for question in self.questions])
            question_text = f"\n{textwrap.indent(question_text, subsequent_indent)}"

        terminal = " terminal" if self.terminal else ""
        return textwrap.indent(
            f"<{self.__class__.__qualname__} {self.get_position()}{terminal}>{question_text}",
            initial_indent,
        )

    @property
    def root_branch(self):
        return (self.tree or self.root).branch

    @property
    def is_first_page(self):
        # this page is the zeroth of the pages directly connected to the tree
        return self.tree is not None and self.index == 0

    @property
    def is_last_page(self):
        if self.terminal:
            return True

        if self.tree is None and self.root is None:
            # this page is not connected to a tree or root page
            # this will most often occur during testing
            return False

        if self.branch or self.navigate is not None:
            # this page either already has a branch
            # or will get a new branch when submitted
            return False

        page = self
        while page is page.root_branch[-1]:
            page = page.root
            if page is None:
                return True

        return False

    @property
    def is_valid(self):
        """
        Returns
        -------
        valid : bool
            Indicator that all of the participant's responses are valid. That
            is, that there are no error messages on the page or any of its
            questions.
        """
        return all([question.is_valid in (True, None) for question in self.questions])

    def get_position(self):
        indices = []
        page = self
        while page is not None:
            indices.append(str(page.index))
            page = page.root
        indices.reverse()
        return ".".join(indices)

    def display(self):
        # we remove the vh-100 class from the div tag wrapping the form and add it back
        # after displaying in a notebook.
        # the vh-100 class makes sure the form extends from the top to the botton of
        # the screen, but we don't want this when displaying in Jupyter
        div_class = self.html_settings["div"]["class"]
        vh_100 = "vh-100" in div_class
        if vh_100:
            div_class = self.html_settings["div"]["class"].copy()
            self.html_settings["div"]["class"].remove("vh-100")

        return_value = display.HTML(self.render(for_notebook_display=True))

        if vh_100:
            self.html_settings["div"]["class"] = div_class

        return return_value

    def clear_feedback(self):
        [question.clear_feedback() for question in self.questions]
        return self

    def clear_responses(self):
        """
        Clear the response from all of this page's questions.

        Returns
        -------
        self : hemlock.Page
        """
        [question.clear_responses() for question in self.questions]
        return self

    def render(self, for_notebook_display=False):
        return render_template(
            self.template,
            page=self,
            navbar=None,
            for_notebook_display=for_notebook_display,
        )

    def get(self, for_notebook_display=False):
        if self.direction_to not in ("back", "invalid") or self.rerun_compile_functions:
            [func(self) for func in self.compile]
            [question.run_compile_functions() for question in self.questions]

        html = self.render(for_notebook_display)
        self.timer.start()
        return html

    def post(self):
        self.timer.pause()

        # record form data
        self.direction_from = request.form.get("direction")
        [question.record_response() for question in self.questions]

        if self.direction_from == "forward":
            # validate user responses
            self.clear_feedback()
            [question.run_validate_functions() for question in self.questions]

            if self.is_valid:
                # record data and run submit and navigate functions
                [question.record_data() for question in self.questions]

                [func(self) for func in self.submit]
                [question.run_submit_functions() for question in self.questions]

                if self.navigate is not None:
                    branch = self.navigate(self)
                    if not is_instance(branch, list):
                        branch = [branch]
                    self.branch = branch
            else:
                self.direction_from = "invalid"

        return self.direction_from
