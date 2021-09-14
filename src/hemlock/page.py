from __future__ import annotations

import copy
import os
import textwrap
from random import sample
from typing import Any, Callable, Collection, List, Mapping, Union

from IPython import display
from flask import render_template, request
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.orm import validates
from sqlalchemy_mutable.html import HTMLSettingType
from sqlalchemy_mutable.types import HTMLSettingsType, MutablePickleType
from sqlalchemy_mutable.utils import is_instance

from ._custom_types import MutableListPickleType
from .app import db
from .utils.format import convert_markdown
from .utils.random import make_hash

HASH_LENGTH = 10
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def compile_questions(page):
    [question.run_compile_functions() for question in page.questions]


def validate_questions(page):
    [question.run_validate_functions() for question in page.questions]


def submit_questions(page):
    [question.run_submit_functions() for question in page.questions]


def debug_questions(page):
    [
        question.fun_debug_functions()
        for question in sample(page.questions, k=len(page.questions))
    ]


class Page(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    defaults = dict(
        navbar=None,
        error=None,
        back=False,
        forward=True,
        template="hemlock/page.html",
        compile=compile_questions,
        validate=validate_questions,
        submit=submit_questions,
        navigate=None,
        debug=debug_questions,
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
            "error": {"class": ["alert", "alert-danger", "w-100"]},
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

    # embedded = db.relationship(
    #     "Embedded",
    #     backref="page",
    #     order_by="Embedded.index",
    #     collection_class=ordering_list("index")
    # )

    # TODO add relationship for timer

    questions = db.relationship(
        "Question",
        backref="page",
        order_by="Question.index",
        collection_class=ordering_list("index"),
    )

    # HTML attributes
    hash = db.Column(db.String(HASH_LENGTH))
    navbar = db.Column(db.Text)
    error = db.Column(db.Text)
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
    validate = db.Column(MutableListPickleType)
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
        navbar=None,
        error: str = None,
        back: Union[bool, str] = None,
        prev_page: Page = None,
        forward: Union[bool, str] = None,
        next_page: Page = None,
        template: str = "hemlock/page.html",
        compile: Union[Callable, List[Callable]] = compile_questions,
        rerun_compile_functions: bool = None,
        validate: Union[Callable, List[Callable]] = validate_questions,
        submit: Union[Callable, List[Callable]] = submit_questions,
        navigate: Callable = None,
        debug: Union[Callable, List[Callable]] = debug_questions,
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

        if is_instance(error, str):
            error = textwrap.dedent(error).strip()
        set_attribute("error", error)
        set_attribute("navbar", navbar, True)
        set_attribute("back", back)
        self.prev_page = prev_page
        set_attribute("forward", forward)
        self.next_page = next_page
        set_attribute("template", template)

        set_attribute("compile", compile, True)
        set_attribute("rerun_compile_functions", rerun_compile_functions)
        set_attribute("validate", validate, True)
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

        return textwrap.indent(
            f"<{self.__class__.__qualname__} id: {self.id}>{question_text}",
            initial_indent,
        )

    @property
    def root_branch(self):
        return (self.tree or self.root).branch

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

    def clear_errors(self):
        """
        Clear the error message from this page and all of its questions.

        Returns
        -------
        self : hemlock.Page
        """
        self.error = None
        for question in self.questions:
            question.error = None
        return self

    def clear_responses(self):
        """
        Clear the response from all of this page's questions.

        Returns
        -------
        self : hemlock.Page
        """
        [question.clear_response() for question in self.questions]
        return self

    def is_first_page(self):
        # this page is the zeroth of the pages directly connected to the tree
        return self.tree is not None and self.index == 0

    def is_last_page(self):
        if self.tree is None and self.root is None:
            return False

        if self is self.root_branch[-1] and self.root is None:
            return True

        if self.branch or self is not self.root_branch[-1]:
            return False

        page = self.root
        while page is page.root_branch[-1]:
            page = page.root
            if page is None:
                return True

        return False

    def is_valid(self):
        """
        Returns
        -------
        valid : bool
            Indicator that all of the participant's responses are valid. That
            is, that there are no error messages on the page or any of its
            questions.
        """
        return not (self.error or any([question.error for question in self.questions]))

    def render(self, for_notebook_display=False):
        return render_template(
            self.template,
            page=self,
            navbar=None,
            error=None if self.error is None else convert_markdown(self.error),
            for_notebook_display=for_notebook_display,
        )

    def get(self, for_notebook_display=False):
        if self.direction_to not in ("back", "invalid") or self.rerun_compile_functions:
            [func(self) for func in self.compile]
        return self.render(for_notebook_display)

    def post(self):
        # record form data
        self.direction_from = request.form.get("direction")
        [question.record_response() for question in self.questions]

        if self.direction_from == "forward":
            # validate user responses
            self.clear_errors()
            for func in self.validate:
                self.error = func(self)
                if self.error:
                    break

            if self.is_valid():
                # record data and run submit and navigate functions
                [question.record_data() for question in self.questions]
                [func(self) for func in self.submit]
                if self.navigate is not None:
                    branch = self.navigate(self)
                    if not isinstance(branch, list):
                        branch = [branch]
                    self.branch = branch
            else:
                self.direction_from = "invalid"

        return self.direction_from
