"""User.
"""
from __future__ import annotations

import functools
import logging
import warnings
from collections import defaultdict
from datetime import datetime
from typing import (
    TYPE_CHECKING,
    Any,
    Callable,
    Dict,
    List,
    Mapping,
    Optional,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import pandas as pd
from flask import current_app, request
from flask_login import UserMixin, current_user, login_required, login_user
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.ext.orderinglist import ordering_list
from sqlalchemy.types import JSON
from sqlalchemy_mutable.types import MutablePickleType, MutableDictJSONType
from sqlalchemy_mutable.utils import is_callable
from werkzeug.wrappers.response import Response

from ._data_frame import DataFrame
from .app import bp, db, login_manager
from .tree import Tree
from .utils.random import make_hash

if TYPE_CHECKING:  # pragma: no cover
    from .page import Page
    from .questions.base import Question

HASH_LENGTH = 90

BranchType = List["Page"]
SeedFunctionType = Callable[[], BranchType]
UserType = TypeVar("UserType", bound="User")
ResponsesType = Union[List[Any], Dict["Question", Any]]

logging.basicConfig(level=logging.INFO)


@login_manager.user_loader
def load_user(user_id: int) -> User:
    """Load user.

    Args:
        user_id (int): User id.

    Returns:
        User: Loaded user.
    """
    return User.query.get(user_id)


class User(UserMixin, db.Model):
    """User.

    The user has the following responsibilities:

    1. The user object contains a list of branches. Based on the URL rule of a request, the user determines which of its trees should process the request.
    2. The user object stores the data for individual users and can collect the data for all users.
    3. The user provides testing utilities.

    Args:
        meta_data (Mapping, optional): User metadata. In an online study, this records
            the user's IP address and any request arguments. Defaults to None.

    Attributes:
        trees (List[Tree]): Trees that the user can navigate to.
        start_time (datetime.datetime): Time at which the user started the study.
        end_time (datetime.datetime): Time at which the user ended the study.
        completed (bool): Indicates that the user completed the study.
        failed (bool): Indicates that the user failed the study.
        errored (bool): Indicates that the user experienced an error.
        in_progress (bool): Indicates that the user is working on the study.
        params (Any): Additional parameters.
        meta_data (Dict[str, Any]): User metadata. In most studies, this will contain
            the IP address.

    Examples:

        .. code-block::

            >>> from hemlock import User, Page, create_test_app
            >>> from hemlock.questions import Input, Label
            >>> from sqlalchemy_mutable.utils import partial
            >>> def greet_user(greeting_label, name_input):
            ...     greeting_label.label = f"Hello, {name_input.response}!"
            ...
            >>> def seed():
            ...     return [
            ...         Page(
            ...             name_input:=Input("What's your name?")
            ...         ),
            ...         Page(
            ...             Label(compile=partial(greet_user, name_input))
            ...         )
            ...     ]
            ...
            >>> app = create_test_app()
            >>> user = User.make_test_user(seed)
            >>> user.test_get().page
            <Page 0>
                <Input What's your name? - default: None>
            >>> user.test_request(["World"]).page
            <Page 1 terminal>
                <Label Hello, World! - default: None>
    """

    _seed_funcs: Dict[str, Tuple[int, SeedFunctionType]] = {}
    default_url_rule: Optional[str] = None

    id = db.Column(db.Integer, primary_key=True)

    trees = db.relationship(
        "Tree", order_by="Tree.index", collection_class=ordering_list("index")
    )

    @classmethod
    def route(
        cls, url_rule: str, default: bool = False
    ) -> Callable[[SeedFunctionType], SeedFunctionType]:
        """Register a user route.

        Args:
            url_rule (str): URL rule associated with this route.
            default (bool, optional): Indicates that this should be the user's default
                route. Defaults to False.

        Returns:
            Callable[[SeedFunctionType], SeedFunctionType]: Route decorator.

        Examples:

            .. doctest::

                >>> from hemlock import User, Page, create_test_app
                >>> @User.route("/survey")
                ... def seed():
                ...     return Page(
                ...         Label("Hello, world!")
                ...     )
                ...
                >>> app = create_test_app()
                >>> user = User.make_test_user()
                >>> user.test_get().page
                <Page 0 terminal>
                    <Label Hello, world! - default: None>
        """

        def register(seed_func: SeedFunctionType) -> SeedFunctionType:
            if url_rule in cls._seed_funcs:
                warnings.warn(
                    f"The url rule '{url_rule}' has already been registered.",
                    RuntimeWarning,
                )
                cls._seed_funcs[url_rule] = cls._seed_funcs[url_rule][0], seed_func
                return seed_func

            @bp.route(url_rule, methods=["GET", "POST"])
            @login_required
            @functools.wraps(seed_func)
            def view_function():
                return current_user.process_request(url_rule)

            index = 0
            if cls._seed_funcs:
                index = list(cls._seed_funcs.values())[-1][0] + 1
            cls._seed_funcs[url_rule] = index, seed_func

            return seed_func

        if default or cls.default_url_rule is None:
            cls.default_url_rule = url_rule

        return register

    hash = db.Column(db.String(HASH_LENGTH))
    start_time = db.Column(db.DateTime)
    end_time = db.Column(db.DateTime)
    params = db.Column(MutablePickleType)
    meta_data = db.Column(MutableDictJSONType)
    errored = db.Column(db.Boolean)
    _cached_data = db.Column(JSON)

    _completed = db.Column(db.Boolean)

    @hybrid_property
    def completed(self) -> Optional[bool]:
        """Indicates that the user completed the study."""
        return self._completed

    @completed.setter  # type: ignore
    def completed(self, completed: bool) -> None:
        """Set the completion status. Cache the user's data when he completes the study."""
        # Note: We need to set completed first so the meta_data reflect that the user
        # has completed the survey when caching the metadata.
        self._completed = completed
        if completed:
            if self.failed:
                warnings.warn(
                    "Indicating that the user completed the study, but the user has already failed the study.",
                    RuntimeWarning,
                )
            self.cache_data()

    _failed = db.Column(db.Boolean)

    @hybrid_property
    def failed(self) -> bool:
        """Indicate that the user failed the study."""
        return self._failed

    @failed.setter  # type: ignore
    def failed(self, failed: bool) -> None:
        """Set the failed status. Cache the user's data when he fails the study."""
        self._failed = failed
        if failed:
            if self.completed:
                warnings.warn(
                    "Indicating that the user failed the study, but the user has already completed the study.",
                    RuntimeWarning,
                )
            self.cache_data()

    @hybrid_property
    def in_progress(self):
        return not (self.completed or self.failed or self.errored)

    def __init__(self, meta_data: Mapping = None):
        self.hash = make_hash(HASH_LENGTH)
        self.start_time = self.end_time = datetime.utcnow()
        self.completed = self.failed = self.errored = False  # type: ignore
        self.meta_data = meta_data or {}

        # need to login user before initializing trees so that the current_user object
        # will be available in the seed functions
        db.session.add(self)
        db.session.commit()
        self._cached_data = self.get_data(to_pandas=False)
        login_user(self)
        self.trees = [Tree(func) for _, func in self._seed_funcs.values()]

    def __repr__(self):
        return f"<{self.__class__.__qualname__} {self.get_meta_data(True)}>"

    def get_tree(self, url_rule: str = None) -> Tree:
        """Get the tree associated with the given URL rule.

        Args:
            url_rule (str, optional): URL rule. Defaults to None.

        Returns:
            Tree: Tree associated with the URL rule.
        """
        # get the index of the requested tree
        index = self._seed_funcs[url_rule or self.default_url_rule][0]  # type: ignore
        return self.trees[index]

    def cache_data(self) -> None:
        """Cache the user's data.
        """
        self._cached_data = self.get_data(to_pandas=False, use_cached_data=False)

    def get_meta_data(self, convert_datetime_to_string: bool = False) -> Dict[str, Any]:
        """Get the user's metadata.

        Args:
            convert_datetime_to_string (bool, optional): Indicates that the user's start
                and end times should be converted to a string. Defaults to False.

        Returns:
            Dict[str, Any]: User's metadata. This is the ``user.meta_data`` attribute
                plus other metadata such as the start and end time.
        """
        metadata = {
            "id": self.id,
            "completed": self.completed,
            "failed": self.failed,
            "errored": self.errored,
            "in_progress": self.in_progress,
            "start_time": self.start_time,
            "end_time": self.end_time,
            "total_seconds": (self.end_time - self.start_time).total_seconds(),
        }
        if convert_datetime_to_string:
            metadata["start_time"] = str(self.start_time)
            metadata["end_time"] = str(self.end_time)

        metadata.update(self.meta_data)
        return metadata

    def get_data(
        self, to_pandas: bool = True, use_cached_data: bool = True
    ) -> Union[pd.DataFrame, DataFrame]:
        """Get the user's data.

        Args:
            to_pandas (bool, optional): Indicates that the data should be returned as a
                pandas dataframe. Defaults to True.
            use_cached_data (bool, optional): Indicates that cached data should be used
                instead of re-collecting the data if possible. Defaults to True.

        Returns:
            Union[pd.DataFrame, DataFrame]: User's data.
        """
        if use_cached_data and self._cached_data is not None:
            df = self._cached_data
        else:
            meta_data = self.get_meta_data(convert_datetime_to_string=True)
            meta_data = {key: [item] for key, item in meta_data.items()}
            df = DataFrame(meta_data, fill_rows=True)
            [df.add_branch(tree.branch) for tree in self.trees]
            df.pad()

        return pd.DataFrame(df) if to_pandas else df

    @staticmethod
    def get_all_data(
        to_pandas: bool = True, refresh_if_in_progress: bool = False
    ) -> Union[pd.DataFrame, DataFrame]:
        """Get the data for all users.

        Args:
            to_pandas (bool, optional): Indicates. Defaults to True.
            refresh_if_in_progress (bool, optional): Refresh data for in progress users
                when getting their data. Setting this to True can greatly increase the
                runtime. Defaults to False.

        Returns:
            Union[pd.DataFrame, DataFrame]: Data from all users.
        """
        df = DataFrame()
        for user in User.query.all():
            if refresh_if_in_progress and user.in_progress:
                df.add_data(user.get_data(to_pandas=False, use_cached_data=False))
            else:
                df.add_data(user.get_data(to_pandas=False))
            df.pad()

        return pd.DataFrame(df) if to_pandas else df

    def process_request(self, url_rule: str) -> Union[str, Response]:
        """Process a request.

        Args:
            url_rule (str): Requested URL rule.

        Returns:
            Union[str, Response]: HTML of the next page.
        """
        if request.method == "POST":
            self.end_time = datetime.utcnow()

        current_tree = self.get_tree(url_rule)
        return_value = current_tree.process_request()

        if (
            not self.failed
            and current_tree.page.is_last_page
            and [tree.page.is_last_page for tree in self.trees]
        ):
            self.completed = True  # type: ignore

        db.session.commit()
        return return_value

    @classmethod
    def make_test_user(
        cls: Type[UserType],
        seed_func: SeedFunctionType = None,
        url_rule: str = "/test",
        **kwargs: Any,
    ) -> UserType:
        """Create a user object for testing.

        Args:
            seed_func (SeedFunctionType, optional): Function that returns the user's
                first branch. Defaults to None.
            url_rule (str, optional): Default URL rule for the test user. Defaults to
                "/test".
            kwargs (Any): Passed to :class:`User` constructor.

        Returns:
            UserType: Test user object.

        Examples:

            .. doctest::

                >>> from hemlock import User, Page, create_test_app
                >>> from hemlock.questions import Label
                >>> app = create_test_app()
                >>> def seed():
                ...     return Page(
                ...         Label("Hello, world!")
                ...     )
                ...
                >>> user = User.make_test_user(seed)
                >>> user.test_get().page
                <Page 0 terminal>
                    <Label Hello, world! - default: None>
        """
        with current_app.test_request_context():
            user = cls(**kwargs)

            if seed_func is not None:
                index = 0
                if user._seed_funcs:
                    index = list(user._seed_funcs.values())[-1][0] + 1
                user._seed_funcs = user._seed_funcs.copy()
                user._seed_funcs[url_rule] = index, seed_func
                user.default_url_rule = url_rule
                user.trees.append(Tree(seed_func, url_rule))

        return user

    @classmethod
    def test_multiple_users(
        cls,
        n_users: int = 1,
        seed_func: SeedFunctionType = None,
        user_kwargs: Mapping[str, Any] = None,
        test_kwargs: Mapping[str, Any] = None,
    ) -> None:
        """Run multiple test users through a study.

        Args:
            n_users (int, optional): Number of users to run. Defaults to 1.
            seed_func (SeedFunctionType, optional): Function that returns the user's
                first branch. Defaults to None.
            user_kwargs (Mapping[str, Any], optional): Passed to
                :meth:`User.make_test_user`. Defaults to None.
            test_kwargs (Mapping[str, Any], optional): Passed to :meth:`User.test`.
                Defaults to None.

        Examples:

            .. code-block::

                >>> from hemlock import User, Page, create_test_app
                >>> from hemlock.questions import Label
                >>> def seed():
                ...     return [
                ...         Page(
                ...             Label("Hello, world!")
                ...         ),
                ...         Page()
                ...     ]
                ...
                >>> app = create_test_app()
                >>> User.test_multiple_users(2, seed)
                INFO:root:TESTING USER 1
                INFO:root:<Page 0>
                    <Label Hello, world! - default: None>
                        test response: None
                    test direction: 'forward'
                INFO:root:<Page 1 terminal>
                INFO:root:FINISHED TESTING USER 1

                INFO:root:TESTING USER 2
                INFO:root:<Page 0>
                    <Label Hello, world! - default: None>
                        test response: None
                    test direction: 'forward'
                INFO:root:<Page 1 terminal>
                INFO:root:FINISHED TESTING USER 2
        """
        user_kwargs = dict(user_kwargs or {})
        user_kwargs["seed_func"] = seed_func
        test_kwargs = dict(test_kwargs or {})
        test_kwargs.setdefault("verbosity", 1)

        for _ in range(n_users):
            user = cls.make_test_user(**user_kwargs)
            logging.info(f"TESTING USER {user.id}")
            user.test(**test_kwargs)
            logging.info(f"FINISHED TESTING USER {user.id}\n")

    def test(
        self, url_rule: str = None, verbosity: int = 2, max_page_visits: int = 10
    ) -> None:
        """Run the test user through the entire study.

        Args:
            url_rule (str, optional): URL rule to test. Defaults to None.
            verbosity (int, optional): Verbosity 0 gives no output. Verbosity 1
                displays pages and test responses as text. Verbosity 2 additionally
                displays the navigation graph and pages as HTML. Defaults to 2.
            max_page_visits (int, optional): Maximum number of times the user can visit
                the same page before an error is raised. Defaults to 10.

        Raises:
            RuntimeError: If the user visits the same page more times than allowed.
                Likely causes include validate functions that always return False and
                infinite loops.

        Examples:

            .. code-block::

                >>> from hemlock import User, Page, create_test_app
                >>> from hemlock.questions import Label
                >>> def seed():
                ...     return [
                ...         Page(
                ...             Label("Hello, world!")
                ...         ),
                ...         Page()
                ...     ]
                ...
                >>> app = create_test_app()
                >>> User.make_test_user(seed).test(verbosity=1)
                INFO:root:<Page 0>
                    <Label Hello, world! - default: None>
                        test response: None
                    test direction: 'forward'
                INFO:root:<Page 1 terminal>
        """
        page_visits: defaultdict[str, int] = defaultdict(int)

        tree = self.test_get(url_rule=url_rule)
        page_visits[tree.page.get_position()] += 1
        if verbosity == 2:
            tree.display()

        while not tree.page.is_last_page:
            tree = self.test_request(url_rule=url_rule, verbose=verbosity >= 1)
            page_visits[tree.page.get_position()] += 1
            if page_visits[tree.page.get_position()] > max_page_visits:
                raise RuntimeError(
                    f"The test user has visited the same page more than {max_page_visits} times. Check that your validate functions don't always return False and that your survey doesn't contain an infinite loop. The page is\n{tree.page}"
                )
            if verbosity == 2:
                tree.display()

        if verbosity >= 1:
            logging.info(tree.page.print())

    def test_request(
        self,
        responses: ResponsesType = None,
        direction: str = None,
        url_rule: str = None,
        **kwargs,
    ) -> Tree:
        """Test a request.

        This simulates posting responses for the current page and getting the next page.

        Args:
            responses (ResponsesType, optional): Test responses. Defaults to None.
            direction (str, optional): Requested direction. Defaults to "forward".
            url_rule (str, optional): URL rule of the request. Defaults to None.
            **kwargs (Any): Passed to :meth:`User.test_post`.

        Returns:
            Tree: Tree associated with the URL rule.
        """
        self.test_post(
            responses=responses, direction=direction, url_rule=url_rule, **kwargs
        )
        return self.test_get(url_rule)

    def test_get(self, url_rule: str = None) -> Tree:
        """Test a get request.

        Args:
            url_rule (str, optional): URL rule of the request. Defaults to None.

        Returns:
            Tree: Tree associated with the URL rule.
        """
        url_rule = url_rule or self.default_url_rule
        with current_app.test_request_context():
            login_user(self)
            self.process_request(url_rule)  # type: ignore
        return self.get_tree(url_rule)

    def test_post(
        self,
        responses: ResponsesType = None,
        direction: str = None,
        url_rule: str = None,
        verbose: bool = True,
    ) -> Tree:
        """Test a post request.

        Args:
            responses (ResponsesType, optional): Test responses. Defaults to None.
            direction (str, optional): Requested direction. Defaults to "forward".
            url_rule (str, optional): URL rule of the request. Defaults to None.
            verbose (bool, optional): When True, logs the current page and responses.
                Defaults to True.

        Returns:
            Tree: Tree associated with the URL rule.
        """
        url_rule = url_rule or self.default_url_rule
        tree = self.get_tree(url_rule)
        page = tree.page

        # collect manually input responses
        if responses is None:
            responses = {}
        elif isinstance(responses, (list, tuple)):
            responses = {
                question: response
                for question, response in zip(page.questions, responses)
            }
        elif isinstance(responses, Mapping):
            responses = dict(responses)
        else:
            raise ValueError(
                f"Responses should be a list, tuple, or mapping, got {repr(responses)}."
            )

        # add automatic responses
        for question in page.questions:
            if question not in responses:
                if is_callable(question.test_response):
                    responses[question] = question.test_response(question)
                else:
                    responses[question] = question.test_response

        # convert responses to raw responses
        data = {
            question.hash: question.make_raw_test_response(response)
            for question, response in responses.items()
        }

        # set the requested direction
        if direction is None:
            if is_callable(page.test_direction):
                direction = page.test_direction(page)
            else:
                direction = page.test_direction
        data["direction"] = direction

        # log the page and planned responses
        if verbose:
            logging.info(page.print(responses, direction))

        with current_app.test_request_context(method="POST", data=data):
            login_user(self)
            self.process_request(url_rule)  # type: ignore
        return tree
