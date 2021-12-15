from itertools import product

import pytest
from flask_login import current_user
from sqlalchemy_mutable.utils import partial

from hemlock import User, Page
from hemlock.app import create_test_app, db
from hemlock.user import load_user
from hemlock.questions import Input


def seed():
    return [Page(), Page()]


def test_load_user():
    create_test_app()
    user = User.make_test_user()
    db.session.add(user)
    db.session.commit()
    assert load_user(user.id) is user


class TestRoute:
    def clear_routes(self):
        User._seed_funcs.clear()
        User.default_url_rule = None

    def test_single(self):
        self.clear_routes()
        url_rule = "/test_single_rule"

        @User.route(url_rule)
        def test_single_seed():
            return Page()

        create_test_app()
        user = User.make_test_user()

        assert user._seed_funcs == {url_rule: (0, test_single_seed)}
        assert user.default_url_rule == url_rule

        assert user.get_tree() is user.trees[0]
        assert user.get_tree(url_rule) is user.trees[0]

        self.clear_routes()

    def test_multiple(self):
        self.clear_routes()
        url_rules = ("/test_multiple_rule0", "/test_multiple_rule1")

        @User.route(url_rules[0])
        def test_multiple_seed0():
            return Page()

        @User.route(url_rules[1], default=True)
        def test_multiple_seed1():
            return Page()

        create_test_app()
        user = User.make_test_user()

        assert user._seed_funcs == {
            url_rules[0]: (0, test_multiple_seed0),
            url_rules[1]: (1, test_multiple_seed1),
        }
        assert user.default_url_rule == url_rules[1]

        assert user.get_tree() is user.trees[1]
        assert user.get_tree(url_rules[0]) is user.trees[0]
        assert user.get_tree(url_rules[1]) is user.trees[1]

        self.clear_routes()

    def test_manual_seed(self):
        self.clear_routes()
        url_rule = "/test_manual_seed_rule"

        @User.route(url_rule)
        def test_manual_seed():
            return Page()

        def test_seed():
            return [Page(), Page()]

        create_test_app()
        user = User.make_test_user(test_seed)

        assert user._seed_funcs == {
            url_rule: (0, test_manual_seed),
            "/test": (1, test_seed),
        }
        assert user.default_url_rule == "/test"
        assert len(user.get_tree().branch) == 2

        self.clear_routes()

    @pytest.mark.filterwarnings("ignore::RuntimeWarning")
    def test_overwrite(self):
        self.clear_routes()
        url_rule = "/test_overwrite_rule"

        @User.route(url_rule)
        def test_overwrite_seed0():
            return Page()

        @User.route(url_rule)
        def test_overwrite_seed1():
            return [Page(), Page()]

        create_test_app()
        user = User.make_test_user()

        assert user._seed_funcs == {url_rule: (0, test_overwrite_seed1)}
        assert user.default_url_rule == url_rule
        assert len(user.get_tree().branch) == 2

        self.clear_routes()


@pytest.mark.parametrize("property_name", ("completed", "failed"))
def test_completed_and_failed(property_name):
    # test that the user caches data when completing or failing the survey
    user = User.make_test_user()
    setattr(user, property_name, True)
    assert user._cached_data is not None
    assert user._cached_data[property_name]


def test_repr():
    user = User.make_test_user()
    assert repr(user).startswith("<User")
    assert str(user.get_meta_data(convert_to_string=True)) in repr(user)


@pytest.mark.parametrize(
    "meta_data, convert_to_string",
    product((None, {"hello": "world"}), (True, False)),
)
def test_get_meta_data(meta_data, convert_to_string):
    user = User.make_test_user(meta_data=meta_data)
    user_meta_data = user.get_meta_data(convert_to_string=convert_to_string)

    assert user_meta_data["completed"] is False
    assert user_meta_data["failed"] is False

    assert user_meta_data["total_seconds"] == 0
    if convert_to_string:
        assert isinstance(user_meta_data["start_time"], str)
        assert isinstance(user_meta_data["end_time"], str)

    if meta_data is not None:
        for key in meta_data.keys():
            assert user_meta_data[key] == meta_data[key]


class TestGetData:
    variable_name = "variable_name"
    response = "user_response{}"

    def create_test_app(self):
        create_test_app()
        [db.session.delete(user) for user in User.query.all()]
        db.session.commit()

    def make_user(self, n_rows=1, complete_survey=True):
        def seed(n_rows=1):
            return [
                Page(Input(variable=TestGetData.variable_name, n_rows=n_rows)),
                Page(),
                Page(),
            ]

        user = User.make_test_user(partial(seed, n_rows))
        response = self.response.format(user.id)
        user.test_request([response])  # user is now on page 1 of 2
        if complete_survey:
            user.test_request()  # user is now on page 2 of 2
        return user

    def assert_expected_data(self, df, completed=True, refresh_if_in_progress=False):
        assert (df.completed == completed).all()
        # test that all rows have been populated with the same start time
        # this should be true of all metadata variables
        assert (df.start_time == df.start_time[0]).all()
        if completed or refresh_if_in_progress:
            assert (df[self.variable_name] == self.response.format(df.id[0])).all()
        else:
            assert self.variable_name not in df

    @pytest.mark.parametrize("n_rows", (1, 3))
    def test_single_user(self, n_rows):
        self.create_test_app()
        user = self.make_user(n_rows)
        df = user.get_data()
        assert len(df) == n_rows
        self.assert_expected_data(df.reset_index(drop=True))

    @pytest.mark.parametrize(
        "n_users, complete_survey, refresh_if_in_progress",
        product((1, 2), (True, False), (True, False)),
    )
    def test_multiple_users(self, n_users, complete_survey, refresh_if_in_progress):
        self.create_test_app()
        [self.make_user(complete_survey=complete_survey) for _ in range(n_users)]
        df = User.get_all_data(refresh_if_in_progress=refresh_if_in_progress)

        if complete_survey or refresh_if_in_progress:
            assert (df.total_seconds != 0).all()
        else:
            # if you don't refresh the data, users in progress should only have the data
            # from the start of the survey
            assert (df.total_seconds == 0).all()
        for _, user_df in df.groupby("id"):
            self.assert_expected_data(
                user_df.reset_index(drop=True), complete_survey, refresh_if_in_progress
            )

    def test_users_with_different_variables(self):
        self.create_test_app()
        User.make_test_user(meta_data={"variable0": "data0"})
        User.make_test_user(meta_data={"variable1": "data1"})
        User.make_test_user(meta_data={"variable0": "data2"})
        df = User.get_all_data(refresh_if_in_progress=True)

        expected_variable0 = ["data0", None, "data2"]
        for value, expected_value in zip(df["variable0"], expected_variable0):
            assert value == expected_value

        expected_variable1 = [None, "data1", None]
        for value, expected_value in zip(df["variable1"], expected_variable1):
            assert value == expected_value


class TestProcessRequest:
    def test_committed_changes(self):
        # test that all changes have been committed after request
        user = User.make_test_user(seed)
        user.test_request()
        assert user not in db.session.dirty

    @staticmethod
    def set_terminal_to_true(page):
        page.terminal = True

    def test_edge_case(self):
        # test an edge case where a page is set to terminal on compile
        # the user should indicate as having completed the study
        def seed():
            return [Page(compile=self.set_terminal_to_true), Page()]

        user = User.make_test_user(seed)
        user.test_get()
        assert user.completed

    @staticmethod
    def set_failed_to_true(page):
        current_user.failed = True

    def test_user_failed(self):
        def seed():
            return Page(compile=self.set_failed_to_true)

        user = User.make_test_user(seed)
        user.test_get()
        assert user.failed
        assert not user.completed


class TestUserAuthentication:
    # test users should be authenticated during requests
    def test_seed(self):
        def seed():
            assert current_user.is_authenticated
            return Page()

        User.make_test_user(seed)

    @staticmethod
    def assert_user_is_authenticated(page):
        assert current_user.is_authenticated

    def test_get(self):
        def seed():
            return Page(compile=self.assert_user_is_authenticated)

        User.make_test_user(seed).test_get()

    def test_post(self):
        def seed():
            return [Page(submit=self.assert_user_is_authenticated), Page()]

        User.make_test_user(seed).test_post()


class TestTestPost:
    test_response = "test response"

    @staticmethod
    def make_test_user(test_response=None, test_direction=None):
        def seed():
            return [
                Page(Input(test_response=test_response), test_direction=test_direction),
                Page(),
            ]

        return User.make_test_user(seed)

    @staticmethod
    def get_response(user):
        return user.get_tree().branch[0].questions[0].response

    def test_auto_response(self):
        user = self.make_test_user()
        user.test_post()
        response = self.get_response(user)
        assert isinstance(response, str) or response is None

    def test_literal_response(self):
        user = self.make_test_user(self.test_response)
        user.test_post()
        assert self.get_response(user) == self.test_response

    def test_list_response(self):
        user = self.make_test_user()
        user.test_post([self.test_response])
        assert self.get_response(user) == self.test_response

    def test_mapping_response(self):
        user = self.make_test_user()
        question = user.get_tree().page.questions[0]
        user.test_post({question: self.test_response})
        assert self.get_response(user) == self.test_response

    def test_literal_direction(self):
        user = self.make_test_user(test_direction="forward")
        user.test_post()
        assert user.get_tree().page is user.get_tree().branch[1]


class TestTest:
    def test_basic_tree(self):
        User.make_test_user(seed).test(verbosity=1)

    @staticmethod
    def validate(question):
        return False

    def test_max_visits(self):
        # test that an error is raised when the user gets stuck
        # e.g., if a validate function always returns False
        def seed():
            return [Page(Input(validate=self.validate)), Page()]

        with pytest.raises(RuntimeError):
            User.make_test_user(seed).test(verbosity=1)

    def test_multiple_users(self):
        User.test_multiple_users(n_users=3, seed_func=seed)
