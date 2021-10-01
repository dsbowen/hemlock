"""Mixin for question objects.
"""
from __future__ import annotations

import copy
import textwrap
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Union

from flask import render_template, request
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import validates
from sqlalchemy_mutable.html import HTMLSettingType
from sqlalchemy_mutable.types import (
    HTMLSettingsType,
    MutableJSONType,
    MutablePickleType,
)
from sqlalchemy_mutable.utils import get_object, is_instance

from .._custom_types import MutableListJSONType, MutableListPickleType
from ..app import db
from ..data import Data
from ..page import Page
from ..utils.format import convert_markdown
from ..utils.random import make_hash

HASH_LENGTH = 10

CompileType = Callable[["Question"], None]
SubmitType = Callable[["Question"], None]
ValidateReturnType = Union[Optional[bool], Tuple[Optional[bool], str]]
ValidateType = Callable[["Question"], ValidateReturnType]


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
        compile (Union[CompileType, List[CompileType]], optional): Functions run
            before this question renders its HTML. Defaults to None.
        validate (Union[ValidateType, List[ValidateType]], optional): Functions run to
            validate the user's response. Defaults to None.
        submit (Union[SubmitType, List[SubmitType]], optional): Functions run after the
            user has submitted his response. Defaults to None.
        test_response (Any, optional): A response to this question used for testing.
            This may also be a function that takes the question object and returns a
            response. Defaults to None.
        Functions run during debugging. Defaults to None.
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
        compile (List[CompileType]): Functions run before this question renders its
            HTML.
        validate (List[ValidateType]): Functions run to validate the user's response.
        submit (List[SubmitType]): Functions run after the user has submitted his
            response.
        test_response (Any): A response to this question used for testing. This may also
            be a function that takes the question object and returns a response.
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
        test_response=None,
        default=None,
        params=None,
        html_settings={
            "card": {"class": ["card", "my-4"]},
            "label": {"class": ["form-label", "w-100"]},
            "feedback": {"class": [], "style": {"display": "block"}},
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
    def _validates_text(self, key: str, value: Optional[str]) -> Optional[str]:
        return None if value is None else textwrap.dedent(value).strip()

    @hybrid_property
    def is_valid(self) -> bool:
        return self._is_valid

    # Function attributes
    compile = db.Column(MutableListPickleType)
    validate = db.Column(MutableListPickleType)
    submit = db.Column(MutableListPickleType)
    test_response = db.Column(MutablePickleType)

    # Additional attributes
    default = db.Column(MutableJSONType)
    raw_response = db.Column(MutableJSONType)
    params = db.Column(MutablePickleType)

    @hybrid_property
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
        compile: Union[CompileType, List[CompileType]] = None,
        validate: Union[ValidateType, List[ValidateType]] = None,
        submit: Union[SubmitType, List[SubmitType]] = None,
        test_response: Any = None,
        default: Any = None,
        params: Any = None,
        extra_html_settings: Mapping[str, HTMLSettingType] = None,
        **kwargs,
    ):
        self.hash = make_hash(HASH_LENGTH)

        self.html_settings = copy.deepcopy(self.defaults["html_settings"])
        if extra_html_settings is not None:
            self.html_settings.update_settings(extra_html_settings)  # type: ignore

        self._set_default_attribute("label", label)
        self._set_default_attribute("floating_label", floating_label)
        self._set_default_attribute("template", template)
        self._set_default_attribute("prepend", prepend, True)
        self._set_default_attribute("append", append, True)
        self._set_default_attribute("form_text", form_text)

        self._set_default_attribute("compile", compile, True)
        self._set_default_attribute("validate", validate, True)
        self._set_default_attribute("submit", submit, True)
        self._set_default_attribute("test_response", test_response, True)

        self._set_default_attribute("default", default, True)
        self._set_default_attribute("params", params, True)

        super().__init__(**kwargs)

    def _set_default_attribute(
        self, name: str, value: Any, copy_default: bool = True
    ) -> None:
        """Set an attribute with a given or default value.

        Args:
            name (str): Name of the attribute.
            value (Any): Given value. If None, use the default value.
            copy_default (bool, optional): Indicates that default value should be
                copied when setting the attribute. Defaults to True.
        """
        if value is None:
            value = self.defaults[name]
            if copy_default:
                value = copy.deepcopy(value)

        setattr(self, name, value)

    def __hash__(self):
        return hash(self.hash)

    def __repr__(self):
        label = None if self.label is None else textwrap.shorten(self.label, 40)

        prefix = "default" if self.raw_response is None else "response"
        default_value = self.default if self.raw_response is None else self.response
        default_text = textwrap.shorten(repr(get_object(default_value)), 40)

        return f"<{self.__class__.__qualname__} {label} - {prefix}: {default_text}>"

    def display(self):
        """Display this question in a notebook."""
        return Page(self, back=False, forward=False).display()

    def clear_feedback(self) -> None:
        """Clear the feedback."""
        self.feedback = None
        self.set_is_valid(None)

    def clear_response(self) -> None:
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
        return self.default if self.raw_response is None else self.raw_response

    def set_is_valid(self, is_valid: bool = None) -> None:
        """Set the indicator that the user's response was valid.

        Additionally adds appropriate validation classes to the feedback tag.

        Args:
            is_valid (bool, optional): Indicates that the response was valid. Defaults
                to None.
        """
        valid_class, invalid_class = "valid-feedback", "invalid-feedback"
        if is_valid is None:
            self._add_and_remove_classes(
                "feedback", remove=[valid_class, invalid_class]
            )
        elif is_valid:
            self._add_and_remove_classes(
                "feedback", add=valid_class, remove=invalid_class
            )
        else:
            self._add_and_remove_classes(
                "feedback", add=invalid_class, remove=valid_class
            )
        self._is_valid = is_valid

    def _add_and_remove_classes(
        self,
        tag_name: str,
        add: Union[str, List[str]] = None,
        remove: Union[str, List[str]] = None,
    ) -> None:
        """Add and remove classes from a given HTML tag.

        Args:
            tag_name (str): Name of the HTML tag.
            add (Union[str, List[str]], optional): Classes to add. Defaults to None.
            remove (Union[str, List[str]], optional): Classes to remove. Defaults to
                None.
        """
        classes = self.html_settings[tag_name]["class"]

        if remove is not None:
            if not isinstance(remove, list):
                remove = [remove]
            for class_name in remove:
                try:
                    classes.remove(class_name)
                except ValueError:
                    pass

        if add is not None:
            if not isinstance(add, list):
                add = [add]
            for class_name in add:
                if class_name not in classes:
                    classes.append(class_name)

    def run_compile_functions(self) -> None:
        """Run the compile functions."""
        [func(self) for func in self.compile]

    def render(self) -> str:
        """Render the HTML.

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

    def record_response(self) -> None:
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

    def record_data(self) -> None:
        """Record the question's data based on the user's response."""
        self.data = self.response

    def run_submit_functions(self) -> None:
        """Run submit functions."""
        [func(self) for func in self.submit]

    def make_raw_test_response(self, response: Any) -> Any:
        """Create a raw rest response from a given test response.

        This is the inverse operation of the :meth:`Question.response` property. It
        converts test responses input by programmers to raw responses used in test
        request contexts.

        Args:
            response (Any): Test response.

        Returns:
            Any: Raw test response.
        """
        return "" if response is None else response
