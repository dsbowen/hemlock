from __future__ import annotations

import copy
import html
import textwrap
from typing import Any, Callable, List, Mapping, Union

from flask import render_template, request
from sqlalchemy.orm import validates
from hemlock.page import HASH_LENGTH
from sqlalchemy_mutable.html import HTMLSettingType
from sqlalchemy_mutable.types import (
    HTMLSettingsType,
    MutableJSONType,
    MutablePickleType,
)
from sqlalchemy_mutable.utils import is_instance

from .._custom_types import MutableListPickleType
from ..app import db
from ..base import Data
from ..page import Page
from ..utils.format import convert_markdown
from ..utils.random import make_hash

HASH_LENGTH = 10


class Question(Data):
    id = db.Column(db.Integer, db.ForeignKey("data.id"), primary_key=True)
    question_type = db.Column(db.String)
    __mapper_args__ = {
        "polymorphic_identity": "question",
        "polymorphic_on": question_type,
    }

    defaults = dict(
        label=None,
        error=None,
        template="hemlock/question.html",
        prepend=None,
        append=None,
        compile=None,
        validate=None,
        submit=None,
        debug=None,
        default=None,
        params=None,
        html_settings={
            "card": {"class": ["card", "my-4"]},
            "label": {"class": ["form-label", "w-100"]},
            "error": {"class": ["alert", "alert-danger"]},
        },
    )

    @property
    def user(self):
        return None if self.page is None else self.page.user

    @property
    def branch(self):
        return None if self.page is None else self.page.branch

    _page_id = db.Column(db.Integer, db.ForeignKey("page.id"))

    # HTML attributes
    hash = db.Column(db.String(HASH_LENGTH))
    label = db.Column(db.Text)
    error = db.Column(db.Text)
    template = db.Column(db.String)
    prepend = db.Column(db.String)
    append = db.Column(db.String)
    html_settings = db.Column(HTMLSettingsType)

    # Function attributes
    compile = db.Column(MutableListPickleType)
    validate = db.Column(MutableListPickleType)
    submit = db.Column(MutableListPickleType)
    debug = db.Column(MutableListPickleType)

    # Additional attributes
    default = db.Column(MutableJSONType)
    response = db.Column(MutableJSONType)
    has_responded = db.Column(db.Boolean, default=False)
    params = db.Column(MutablePickleType)

    def __init__(
        self,
        label: str = None,
        error: str = None,
        template: str = None,
        prepend: str = None,
        append: str = None,
        compile: Union[Callable, List[Callable]] = None,
        validate: Union[Callable, List[Callable]] = None,
        submit: Union[Callable, List[Callable]] = None,
        debug: Union[Callable, List[Callable]] = None,
        default: Any = None,
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

        if is_instance(label, str):
            label = textwrap.dedent(label).strip()
        set_attribute("label", label)

        if is_instance(error, str):
            error = textwrap.dedent(error).strip()
        set_attribute("error", error)

        set_attribute("template", template)
        set_attribute("prepend", prepend)
        set_attribute("append", append)

        set_attribute("compile", compile, True)
        set_attribute("validate", validate, True)
        set_attribute("submit", submit, True)
        set_attribute("debug", debug, True)

        set_attribute("default", default, True)
        set_attribute("params", params, True)

        self.html_settings = copy.deepcopy(self.defaults["html_settings"])
        if extra_html_settings is not None:
            self.html_settings.update_settings(extra_html_settings)

    def __repr__(self):
        label = None if self.label is None else textwrap.shorten(self.label, 40)

        if self.has_responded:
            prefix = "response"
            response = self.response
        else:
            prefix = "default"
            response = self.default
        if is_instance(response, str):
            response = textwrap.shorten(response, 40)

        return f"<{self.__class__.__qualname__} {label} - {prefix}: {response}>"

    def display(self):
        return Page(self, forward=False).display()

    def clear_response(self):
        """
        Clear the response.

        Returns
        -------
        self : hemlock.Question
        """
        self.response = None
        self.has_responded = False
        return self

    def run_compile_functions(self):
        [func(self) for func in self.compile]
        return self

    def render(self):
        return render_template(
            self.template,
            question=self,
            label=None if self.label is None else convert_markdown(self.label),
            error=None if self.error is None else convert_markdown(self.error),
        )

    def record_response(self):
        self.has_responded = True
        self.response = request.form.get(self.hash)
        if self.response == "":
            # participant did not respond
            self.response = None
        return self

    def run_validate_functions(self):
        """Validate Participant response

        Check validate functions one at a time. If any yields an error
        message (i.e. error is not None), indicate the response was invalid
        and return False. Otherwise, return True.
        """
        for func in self.validate:
            self.error = func(self)
            if self.error:
                return False

        self.error = None
        return True

    def record_data(self):
        self.data = self.response
        return self

    def run_submit_functions(self):
        [func(self) for func in self.submit]
        return self

    def run_debug_functions(self):
        [func(self) for func in self.debug]
        return self
