"""Mixin for question objects.
"""
from __future__ import annotations

import copy
import textwrap
from typing import Any, Callable, Dict, List, Mapping, Union

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

from .._custom_types import MutableListJSONType, MutableListPickleType
from ..app import db
from ..data import Data
from ..page import Page
from ..utils.format import convert_markdown
from ..utils.random import make_hash

HASH_LENGTH = 10


class Question(Data):
    """Mixin for question objects.

    Args:
        label (str, optional): Question label, prompt, or instructions. Defaults to None.
        floating_label (str, optional): Label that floats in the input tag. Defaults
            to None.
        template (str, optional): Path to a jinja template. Defaults to None.
        prepend (Union[str, List[str]], optional): Text prepended to the input tag.
            Defaults to None.
        append (Union[str, List[str]], optional): Text appended to the input tag.
            Defaults to None.
        form_text (str, optional): Form text which usually appears below an input.
            Defaults to None.
        compile (Union[Callable, List[Callable]], optional): Functions run before this
            question renders its HTML. Defaults to None.
        validate (Union[Callable, List[Callable]], optional): Functions run to
            validate the user's response. Defaults to None.
        submit (Union[Callable, List[Callable]], optional): Functions run after the
            user has submitted his response. Defaults to None.
        debug (Union[Callable, List[Callable]], optional): Functions run during
            debugging. Defaults to None.
        default (Any, optional): Default response value. Defaults to None.
        params (Any, optional): Additional parameters. Defaults to None.
        extra_html_settings (Mapping[str, HTMLSettingType], optional): Additional HTML
            settings used to update the defaults. Defaults to None.

    Attributes:
        id (int): Unique question identity.
        hash (str): Unique hash.
        page (Page): Page on which this question appears.
        label (str): Question label, prompt, or instructions.
        floating_label (str): Label that floats in the input tag.
        template (str): Path to a jinja template.
        prepend (List[str]): Text prepended to the input tag.
        append (List[str]): Text appended to the input tag.
        form_text (str): Form text which usually appears below an input.
        compile (List[Callable]): Functions run before this question renders its HTML.
        validate (List[Callable]): Functions run to validate the user's response.
        submit (List[Callable]): Functions run after the user has submitted his
            response.
        debug (List[Callable]): Functions run during debugging.
        default (Any): Default response value.
        params (Any): Additional parameters.
        raw_response (Any): User's raw response to the question.
        response (Any): User's repsonse to the question. By default, this is the same
            as the raw response. However, subclasses may convert the raw response to a
            different format or data type for validation and other purposes. Read only.
        feedback (str): Feedback on the user's response.
        is_valid (bool): Indicates that the user's response was valid.
        html_settings (HTMLSettings): HTML settings used by the jinja template.
    """

    id = db.Column(db.Integer, db.ForeignKey("data.id"), primary_key=True)
    question_type = db.Column(db.String)
    __mapper_args__ = {
        "polymorphic_identity": "question",
        "polymorphic_on": question_type,
    }

    defaults: Dict[str, Any] = dict(
        label=None,
        floating_label=None,
        template=None,
        prepend=None,
        append=None,
        form_text=None,
        compile=[],
        validate=[],
        submit=[],
        debug=[],
        default=None,
        params=None,
        html_settings={
            "card": {"class": ["card", "shadow-sm", "my-4"]},
            "label": {"class": ["form-label", "w-100"]},
            "feedback": {"class": []},
        },
    )

    _page_question_id = db.Column(db.Integer, db.ForeignKey("page.id"))

    # HTML attributes
    hash = db.Column(db.String(HASH_LENGTH))
    label = db.Column(db.Text)
    floating_label = db.Column(db.String)
    template = db.Column(db.String)
    prepend = db.Column(MutableListJSONType)
    append = db.Column(MutableListJSONType)
    feedback = db.Column(db.Text)
    _is_valid = db.Column(db.Boolean)
    form_text = db.Column(db.Text)
    html_settings = db.Column(HTMLSettingsType)

    @validates("label", "form_text", "feedback")
    def validates_text(self, key, value):
        return None if value is None else textwrap.dedent(value).strip()

    @property
    def is_valid(self) -> bool:
        return self._is_valid

    # Function attributes
    compile = db.Column(MutableListPickleType)
    validate = db.Column(MutableListPickleType)
    submit = db.Column(MutableListPickleType)
    debug = db.Column(MutableListPickleType)

    # Additional attributes
    default = db.Column(MutableJSONType)
    raw_response = db.Column(MutableJSONType)
    params = db.Column(MutablePickleType)

    @property
    def response(self):
        return None if self.raw_response == "" else self.raw_response

    def __init__(
        self,
        label: str = None,
        floating_label: str = None,
        template: str = None,
        prepend: Union[str, List[str]] = None,
        append: Union[str, List[str]] = None,
        form_text: str = None,
        compile: Union[Callable, List[Callable]] = None,
        validate: Union[Callable, List[Callable]] = None,
        submit: Union[Callable, List[Callable]] = None,
        debug: Union[Callable, List[Callable]] = None,
        default: Any = None,
        params: Any = None,
        extra_html_settings: Mapping[str, HTMLSettingType] = None,
        **kwargs,
    ):
        def set_attribute(name, value, copy_default=False):
            if value is None:
                value = self.defaults[name]
                if copy_default:
                    value = copy.deepcopy(value)

            setattr(self, name, value)

        self.hash = make_hash(HASH_LENGTH)

        self.html_settings = copy.deepcopy(self.defaults["html_settings"])
        if extra_html_settings is not None:
            self.html_settings.update_settings(extra_html_settings)  # type: ignore

        set_attribute("label", label)
        set_attribute("floating_label", floating_label)
        set_attribute("template", template)
        set_attribute("prepend", prepend, True)
        set_attribute("append", append, True)
        set_attribute("form_text", form_text)

        set_attribute("compile", compile, True)
        set_attribute("validate", validate, True)
        set_attribute("submit", submit, True)
        set_attribute("debug", debug, True)

        set_attribute("default", default, True)
        set_attribute("params", params, True)

        super().__init__(**kwargs)

    def __hash__(self):
        return self.hash

    def __repr__(self):
        label = None if self.label is None else textwrap.shorten(self.label, 40)
        prefix = "default" if self.raw_response is None else "response"
        default = self.get_default() or None
        if is_instance(default, str):
            default = textwrap.shorten(default, 40)

        return f"<{self.__class__.__qualname__} {label} - {prefix}: {default}>"

    def display(self):
        """Display this question in a notebook."""
        return Page(self, back=False, forward=False).display()

    def clear_feedback(self):
        """Clear the feedback."""
        self.feedback = None
        self.set_is_valid(None)

    def clear_response(self):
        """Clear the feedback and response."""
        self.raw_response = None
        self.clear_feedback()

    def get_default(self) -> Any:
        """Get the default value.

        If the user has not yet responded, this method returns the default value.
        Otherwise, it returns the user's response.

        Returns:
            Any: Default value.
        """
        if self.raw_response is None:
            if self.default is None:
                return ""

            return self.default

        return self.raw_response

    def set_is_valid(self, is_valid: bool = None):
        """Set the indicator that the user's response was valid.

        Args:
            is_valid (bool, optional): Indicates that the response was valid. Defaults
                to None.
        """
        self._is_valid = is_valid

    def run_compile_functions(self):
        """Run the compile functions."""
        [func(self) for func in self.compile]

    def render(self) -> str:
        """Render the HTML

        Returns:
            str: HTML.
        """

        def render_markdown(text, strip_last_paragraph=False):
            if text is None:
                return None

            return convert_markdown(text, strip_last_paragraph=strip_last_paragraph)

        return render_template(
            self.template,
            question=self,
            label=render_markdown(self.label),
            feedback=render_markdown(self.feedback, True),
            form_text=render_markdown(self.form_text, True),
        )

    def record_response(self):
        """Record the user's response."""
        self.raw_response = request.form.get(self.hash)

    def run_validate_functions(self) -> bool:
        """Run the validate functions to check the user's response.

        This method runs the validate functions one at a time to check for errors. If
        a validate function indicates that the response is invalid, this method sets
        the question's feedback (if given) and validity status and returns.

        Returns:
            bool: Indicates that the response was valid.
        """
        if self.validate:
            for func in self.validate:
                result = func(self)
                if is_instance(result, tuple):
                    # result is (is_valid: Optional[bool], feedback: str)
                    is_valid, self.feedback = result
                else:
                    # result is is_valid: Optional[bool]
                    is_valid, self.feedback = result, None

                if is_valid is False:
                    self.set_is_valid(False)
                    return False

            self.set_is_valid(is_valid)

        return True

    def record_data(self):
        """Record the question's data based on the user's response."""
        self.data = self.response

    def run_submit_functions(self):
        """Run submit functions."""
        [func(self) for func in self.submit]

    def run_debug_functions(self):
        """Run debugging functions."""
        [func(self) for func in self.debug]
