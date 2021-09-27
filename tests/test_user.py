from itertools import product

import pytest
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

    def test_overwrite(self):
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
    assert user._cached_data is None
    setattr(user, property_name, True)
    assert user._cached_data is not None
    assert user._cached_data[property_name]


def test_repr():
    user = User.make_test_user()
    assert repr(user).startswith("<User")
    assert str(user.get_meta_data(convert_datetime_to_string=True)) in repr(user)


@pytest.mark.parametrize(
    "meta_data, convert_datetime_to_string",
    product((None, {"hello": "world"}), (True, False)),
)
def test_get_meta_data(meta_data, convert_datetime_to_string):
    user = User.make_test_user(meta_data=meta_data)
    user_meta_data = user.get_meta_data(
        convert_datetime_to_string=convert_datetime_to_string
    )

    assert user_meta_data["completed"] is False
    assert user_meta_data["failed"] is False

    assert user_meta_data["total_seconds"] == 0
    if convert_datetime_to_string:
        assert isinstance(user_meta_data["start_time"], str)
        assert isinstance(user_meta_data["end_time"], str)

    if meta_data is not None:
        for key in meta_data.keys():
            assert user_meta_data[key] == meta_data[key]


class TestGetData:
    variable_name = "variable_name"
    response = "user_response{}"

    @staticmethod
    def seed(n_rows=1):
        return [
            Page(Input(variable=TestGetData.variable_name, n_rows=n_rows)),
            Page(),
            Page(),
        ]

    def make_user(self, n_rows=1, complete_survey=True):
        user = User.make_test_user(partial(self.seed, n_rows))
        response = self.response.format(user.id)
        user.test_request([response])  # user is now on page 1 of 2
        if complete_survey:
            user.test_request()  # user is now on page 2 of 2
        return user

    def assert_expected_data(self, df, completed=True):
        assert (df.completed == completed).all()
        # test that all rows have been populated with the same start time
        # this should be true of all metadata variables
        assert (df.start_time == df.start_time[0]).all()
        assert (df[self.variable_name] == self.response.format(df.id[0])).all()

    @pytest.mark.parametrize("n_rows", (1, 3))
    def test_single_user(self, n_rows):
        create_test_app()
        [db.session.delete(user) for user in User.query.all()]
        db.session.commit()

        user = self.make_user(n_rows)
        df = user.get_data()
        assert len(df) == n_rows
        self.assert_expected_data(df.reset_index(drop=True))

    @pytest.mark.parametrize(
        "n_users, complete_survey, cached_data_only",
        product((1, 2), (True, False), (True, False)),
    )
    def test_multiple_users(self, n_users, complete_survey, cached_data_only):
        create_test_app()
        [db.session.delete(user) for user in User.query.all()]
        db.session.commit()

        [self.make_user(complete_survey=complete_survey) for _ in range(n_users)]
        df = User.get_all_data(cached_data_only=cached_data_only)

        if not complete_survey and cached_data_only:
            # test that you don't get any data because users haven't completed the
            # survey, meaning they don't have cached data
            assert len(df) == 0
        else:
            assert len(df) == n_users
            for _, user_df in df.groupby("id"):
                self.assert_expected_data(
                    user_df.reset_index(drop=True), complete_survey
                )
