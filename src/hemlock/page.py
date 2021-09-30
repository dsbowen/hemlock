"""Page.
"""
from __future__ import annotations

import copy
import os
import random
import textwrap
from random import sample
from typing import Any, Callable, Dict, List, Mapping, Optional, Tuple, Union

from IPython import display
from flask import render_template, request
from sqlalchemy.ext.hybrid import hybrid_property
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

CompileType = Callable[["Page"], None]
SubmitType = Callable[["Page"], None]
NavigateType = Callable[["Page"], List["Page"]]


def random_direction(page: Page, pr_back: float = 0.2) -> str:
    """Chooses a random direction for navigation.

    Args:
        page (Page): Page to navigate from.
        pr_back (float, optional): Probability of going back if both forward and back
            navigation are available. This parameter is ignored if it is only possible
            to navigate in one direction. Defaults to 0.2.

    Raises:
        ValueError: If it is impossible to navigate from this page.

    Returns:
        str: "forward" or "back"
    """
    forward = bool(page.forward) and not page.is_last_page
    back = bool(page.back) and not page.is_first_page

    if not (forward or back):
        raise ValueError(f"Navigation is not possible from page {page}.")

    if forward and not back:
        return "forward"

    if back and not forward:
        return "back"

    return "back" if random.random() < pr_back else "forward"


class Page(db.Model):
    """Page.

    A page's primary function is to present users with a list of questions then allow
    them to navigate to other pages in the survey.

    Args:
        *questions (Question): Questions for the user.
        timer (Union[str, Timer], optional): Records the amount of time the user spent
            on this page. A string is interpreted as the timer's variable name.
            Defaults to None.
        data (List[Union[Data, Tuple]], optional): Additional data items. Tuple inputs
            are used as arguments to the :class:`hemlock.data.Data` constructor.
            Defaults to None.
        navbar ([type], optional): Navigation bar. Defaults to None.
        back (Union[bool, str], optional): If a bool, indicates that the user can go
            back. If a string, this is the text of the back button. Defaults to None.
        prev_page (Page, optional): The page to which the back button takes the user.
            If None, the back button takes the user to the previous page. Defaults to
            None.
        forward (Union[bool, str], optional): If a bool, indicates that the user can
            go forward. If a string, this is the text of the forward button. Defaults
            to None.
        next_page (Page, optional): The page to which the forward button takes the
            user. If None, the forward button takes the user to the next page.
            Defaults to None.
        template (str, optional): Template used to render the page. Defaults to
            "hemlock/page.html".
        compile (Union[CompileType, List[CompileType]], optional): Functions run
            before this page renders its HTML. Defaults to None.
        rerun_compile_functions (bool, optional): Indicates that compile functions
            should be rerun when the user goes back to this page or if the user's
            responses to this page were invalid. By default, the compile functions are
            only run when the user goes forward to this page. Defaults to None.
        submit (Union[SubmitType, List[SubmitType]], optional): Functions run after
            the user submits his responses. Defaults to None.
        test_direction (Union[str, Callable[[Page], str]], optional): The direction
            ("forward" or "back") to navigate from this page during testing. This may
            also be a function that takes a page and returns a direction. Defaults to
            None.
        navigate (NavigateType, optional): This function runs after the submit
            functions and creates a branch off of this page. Defaults to None.
        terminal (bool, optional): Indicates that this is the last page of the survey.
            Defaults to False.
        params (Any, optional): Additional parameters. Defaults to None.
        extra_html_settings (Mapping[str, HTMLSettingType], optional): Additional HTML
            settings. Defaults to None.

    Attributes:
        tree (Tree): Tree to which this page belongs.
        branch (List[Page]): Pages that branch off of the current page.
        root (Page): The page to whose branch this page belongs.
        index (int): This page's position on its root's branch.
        questions (List[Question]): Questions for the user.
        timer (Timer): Records the amount of time the user spent on this page.
        data (List[Data], optional): Additional data items.
        navbar ([type], optional): Navigation bar.
        back (Optional[str]): The text of the back button. If None, the user cannot go
            back from this page.
        prev_page (Page): The page to which the back button takes the user.
        forward (Optional[str]): The text of the forward button. If None, the user
            cannot go forward from this page.
        next_page (Page, optional): The page to which the forward button takes the
            user.
        template (str): Template used to render the page.
        compile (List[CompileType]): Functions run before this page renders its HTML.
        rerun_compile_functions (bool): Indicates that compile functions should be
            rerun when the user goes back to this page or if the user's responses to
            this page were invalid.
        submit (List[SubmitType]): Functions run after the user submits his responses.
        navigate (NavigateType): This function runs after the submit functions and
            creates a branch off of this page.
        test_direction (Union[str, Callable[[Page], str]]): The direction ("forward" or
            "back") to navigate from this page during testing. This may also be a
            function that takes a page and returns a direction.
        terminal (bool): Indicates that this is the last page of the survey.
        params (Any): Additional parameters.
        html_settings (Mapping[str, HTMLSettingType]): HTML settings.
        direction_from (Optional[str]): Direction which the user is navigating from
            this page. Either "forward", "back", or "invalid".
        direction_to (Optional[str]): Direction which the user navigated to this page.
            Either "forward", "back", or "invalid".

    Examples:

        .. doctest::

            >>> from hemlock import Page
            >>> from hemlock.questions import Input, Label
            >>> Page(
            ...     Label("Hello, world!"),
            ...     Input("What's your name?")
            ... )
            <Page None>
                <Label Hello, world! - default: None>
                <Input What's your name? - default: None>

    Notes:

        Data can be input as :class:`hemlock.data.Data` objects or as tuples. Tuple
        inputs are used as arguments for the ``Data`` constructor.

        .. doctest::

            >>> from hemlock import User, Page, create_test_app
            >>> from hemlock.data import Data
            >>> app = create_test_app()
            >>> def seed():
            ...     return Page(data=[("variable0", 0), Data("variable1", 1)])
            ...
            >>> user = User.make_test_user(seed)
            >>> user.get_data()[["variable0", "variable1"]]
               variable0  variable1
            0          0          1
    """

    id = db.Column(db.Integer, primary_key=True)

    defaults: Dict[str, Any] = dict(
        navbar=None,
        error=None,
        back=False,
        forward=True,
        template="hemlock/page.html",
        compile=[],
        submit=[],
        navigate=None,
        test_direction=random_direction,
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

    questions = db.relationship(
        "Question",
        backref="page",
        order_by="Question.index",
        collection_class=ordering_list("index"),
        foreign_keys="Question._page_question_id",
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

    @validates("data")
    def _validate_data(self, key: str, data: Union[Data, Tuple]) -> Data:
        """Data can be input as a :class:`hemlock.data.Data` object or a tuple.

        Tuple inputs are used as arguments for the ``Data`` constructor.
        """
        return data if isinstance(data, Data) else Data(*data)

    timer = db.relationship("Timer", uselist=False, foreign_keys="Timer._page_timer_id")

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
    ) -> Optional[str]:
        if not value:
            return None

        if value is True:
            return ">>" if key == "forward" else "<<"

        # value is str
        return value  # type: ignore

    # Function attributes
    compile = db.Column(MutableListPickleType)
    submit = db.Column(MutableListPickleType)
    navigate = db.Column(MutablePickleType)
    test_direction = db.Column(MutablePickleType)

    # Additional attributes
    params = db.Column(MutablePickleType)
    direction_from = db.Column(db.String(8))
    direction_to = db.Column(db.String(8))
    index = db.Column(db.Integer)
    terminal = db.Column(db.Boolean, default=False)
    rerun_compile_functions = db.Column(db.Boolean)

    @hybrid_property
    def root_branch(self) -> List[Page]:
        """Get the branch to which this page belongs.

        The root branch is this page's root's branch (implying that this page is on the
        returned branch). The root is either a tree or a root page.

        Returns:
            List[Page]: Branch.
        """
        return (self.tree or self.root).branch

    @hybrid_property
    def is_first_page(self) -> bool:
        """Indicates that this page is the first page (of its tree).

        Returns:
            bool: Indicator.
        """
        # this page is the zeroth of the pages directly connected to the tree
        return self.tree is not None and self.index == 0

    @hybrid_property
    def is_last_page(self) -> bool:
        """Indicates that this page is the last page (of its tree).

        Returns:
            bool: Indicator.
        """
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

    @hybrid_property
    def is_valid(self) -> bool:
        """Indicates that the user's responses to all questions on this page are valid.

        Returns:
            bool: Indicator.
        """
        return all([question.is_valid in (True, None) for question in self.questions])

    def __init__(
        self,
        *questions: hemlock.questions.base.Question,  # type: ignore
        timer: Union[str, Timer] = None,
        data: List[Data] = None,
        navbar=None,  # TODO: typehint for navbar
        back: Union[bool, str] = None,
        prev_page: Page = None,
        forward: Union[bool, str] = None,
        next_page: Page = None,
        template: str = "hemlock/page.html",
        compile: Union[CompileType, List[CompileType]] = None,
        rerun_compile_functions: bool = None,
        submit: Union[SubmitType, List[SubmitType]] = None,
        navigate: NavigateType = None,
        test_direction: Union[str, Callable[[Page], str]] = None,
        terminal: bool = False,
        params: Any = None,
        extra_html_settings: Mapping[str, HTMLSettingType] = None,
    ):
        def set_default_attribute(name, value, copy_default=False):
            if value is None:
                value = self.defaults[name]
                if copy_default:
                    value = copy.deepcopy(value)

            setattr(self, name, value)

        self.hash = make_hash(HASH_LENGTH)

        self.questions = list(questions)
        self.timer = Timer(variable=timer) if is_instance(timer, str) else Timer()
        self.data = [] if data is None else data

        set_default_attribute("navbar", navbar, True)
        set_default_attribute("back", back)
        self.prev_page = prev_page
        set_default_attribute("forward", forward)
        self.next_page = next_page
        set_default_attribute("template", template)

        set_default_attribute("compile", compile, True)
        set_default_attribute("rerun_compile_functions", rerun_compile_functions)
        set_default_attribute("submit", submit, True)
        set_default_attribute("navigate", navigate, True)
        set_default_attribute("test_direction", test_direction, True)

        self.terminal = terminal
        set_default_attribute("params", params, True)

        self.html_settings = copy.deepcopy(self.defaults["html_settings"])
        if extra_html_settings is not None:
            self.html_settings.update_settings(extra_html_settings)  # type: ignore

    def __repr__(self):
        return self.print()

    def print(
        self,
        test_responses: Dict[  #  type: ignore
            "hemlock.questions.base.Question", Any
        ] = None,
        direction: str = None,
    ) -> str:
        """Print the page.

        Args:
            test_responses (Dict[, optional): Maps questions on the page to test
                responses. Defaults to None.
            direction (str, optional): Test direction. Defaults to None.

        Returns:
            str: Page representation.
        """
        initial_indent = ""
        subsequent_indent = 4 * " "

        if not self.questions:
            question_text = ""
        else:
            if test_responses is None:
                question_text = "\n".join(
                    [str(question) for question in self.questions]
                )
            else:
                question_texts = []
                for question in self.questions:
                    test_response = test_responses.get(question)
                    question_texts.append(
                        f"{question}\n{subsequent_indent}test response: {repr(test_response)}"
                    )
                question_text = "\n".join(question_texts)

            question_text = f"\n{textwrap.indent(question_text, subsequent_indent)}"

        if direction is None:
            direction_text = ""
        else:
            direction_text = f"\n{subsequent_indent}test direction: {repr(direction)}"

        terminal = " terminal" if self.is_last_page else ""
        return textwrap.indent(
            f"<{self.__class__.__qualname__} {self.get_position()}{terminal}>{question_text}{direction_text}",
            initial_indent,
        )

    def get_position(self) -> str:
        """Get this page's position on its tree.

        Returns:
            str: Position.
        """
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

    def clear_feedback(self) -> None:
        """Clear feedback on all of this page's questions."""
        [question.clear_feedback() for question in self.questions]

    def clear_responses(self) -> None:
        """Clear the user's responses (and feedback) to all of this page's questions."""
        [question.clear_response() for question in self.questions]

    def render(self, for_notebook_display=False) -> str:
        """Render the HTML.

        Returns:
            str: HTML.
        """
        return render_template(
            self.template,
            page=self,
            navbar=None,
            for_notebook_display=for_notebook_display,
        )

    def get(self, for_notebook_display=False) -> str:
        """Process a GET request.

        Args:
            for_notebook_display (bool, optional): Indicates that this is a test
                user's request and the output will displayed in a notebook. Defaults
                to False.

        Returns:
            str: Rendered HTML.
        """
        if self.direction_to in ("forward", None) or self.rerun_compile_functions:
            [func(self) for func in self.compile]
            [question.run_compile_functions() for question in self.questions]

        html = self.render(for_notebook_display)
        self.timer.start()
        return html

    def post(self) -> str:
        """Process a POST request.

        Returns:
            str: The direction the user should go from this page ("forward", "back",
                or "invalid").
        """
        self.timer.pause()

        # record form data
        self.direction_from = request.form["direction"]
        for question in self.questions:
            question.record_response()

        if self.direction_from == "forward":
            # validate user responses
            self.clear_feedback()
            for question in self.questions:
                question.run_validate_functions()

            if self.is_valid:
                # record data and run submit and navigate functions
                for question in self.questions:
                    question.record_data()

                for func in self.submit:
                    func(self)
                for question in self.questions:
                    question.run_submit_functions()

                if self.navigate is not None:
                    branch = self.navigate(self)
                    if not is_instance(branch, list):
                        branch = [branch]
                    self.branch = branch
            else:
                self.direction_from = "invalid"

        return self.direction_from
