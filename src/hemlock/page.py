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
from .utils.format import convert_markdown
from .utils.random import make_hash

HASH_LENGTH = 10
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def compile_questions(page):
    [question.compile() for question in page.questions]


def validate_questions(page):
    [question.validate() for question in page.questions]


def submit_questions(page):
    [question.submit() for question in page.questions]


def debug_questions(page):
    [question.debug() for question in sample(page.questions, k=len(page.questions))]


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

    _user_head_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    _branch_id = db.Column(db.Integer, db.ForeignKey("branch.id"))

    next_branch = db.relationship(
        "Branch",
        back_populates="prev_page",
        uselist=False,
        foreign_keys="Branch._prev_page_id",
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
        backref="Page",
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

    def __init__(
        self,
        *questions: questions.base.Question,
        navbar=None,
        error: str = None,
        back: Union[bool, str] = False,
        prev_page: Page = None,
        forward: Union[bool, str] = True,
        next_page: Page = None,
        template: str = "hemlock/page.html",
        compile: Union[Callable, List[Callable]] = compile_questions,
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

    def display(self):
        # we remove the vh-100 class from the div tag wrapping the form and add it back
        # after displaying
        # the vh-100 class makes sure the form extends from the top to the botton of
        # the screen, but we don't want this when displaying in Jupyter
        div_class = self.html_settings["div"]["class"]
        vh_100 = "vh-100" in div_class
        if vh_100:
            div_class = self.html_settings["div"]["class"].copy()
            self.html_settings["div"]["class"].remove("vh-100")

        return_value = display.HTML(self.render(display=True))

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
        return (
            self.branch is not None
            and self.branch.prev_page is None
            and self.branch.prev_branch is None
            and self.index == 0
        )

    def is_last_page(self):
        def subtree_has_pages(next_branch):
            while next_branch is not None:
                if next_branch.pages:
                    return True
                next_branch = next_branch.next_branch

            return False

        if self.branch is None or self is not self.branch.pages[-1]:
            return False

        # if this page's next branch or this page's branch's next branch have pages in
        # their subtree, this is not the last page
        for next_branch in (self.next_branch, self.branch.next_branch):
            if subtree_has_pages(next_branch):
                return False

        # look for the next page on a previous branch
        branch = self.branch
        while branch is not None:
            prev_page = branch.prev_page
            if prev_page is not None:
                branch = prev_page.branch
                if prev_page is not branch.pages[-1] or subtree_has_pages(branch.next_branch):
                    return False
            else:
                branch = branch.prev_branch

        return True

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

    def run_compile_functions(self):
        """
        Run the page's compile functions. If `self.cache_compile`, the page's
        compile functions and compile worker are removed.

        Returns
        -------
        self
        """
        if self.run_compile:
            [func(self) for func in self.compile]
            if self.cache_compile:
                self.compile = self.compile_worker = None
            self.run_compile = False
        return self

    def render(self, display=False):
        return render_template(
            self.template,
            page=self,
            navbar=None,
            error=None if self.error is None else convert_markdown(self.error),
            display=display,
        )

    def record_response(self):
        """Record participant response

        Begin by updating the total time. Then get the direction the
        participant requested for navigation (forward or back). Finally,
        record the participant's response to each question.
        """
        self.direction_from = request.form.get("direction")
        [question.record_response() for question in self.questions]
        return self

    def run_validate_functions(self):
        """Validate response

        Check validate functions one at a time. If any returns an error
        message (i.e. error is not None), indicate the response was invalid
        and return False. Otherwise, return True.
        """
        self.clear_errors()
        for func in self.validate:
            self.error = func(self)
            if self.error:
                break

        is_valid = self.is_valid()
        self.direction_from = "forward" if is_valid else "invalid"
        return is_valid

    def run_submit_functions(self):
        [question.record_data() for question in self.questions]
        [func(self) for func in self.submit]
        return self

    def run_navigate_function(self):
        self.next_branch = self.navigate(self)
        return self

    def run_debug_functions(self):
        [func(self) for func in self.debug]
        return self
