import io
import os

import pandas as pd
import pytest

from hemlock import User, Page, create_test_app
from hemlock._admin_routes import password_is_correct, get_user_status
from hemlock.app import Config, db
from hemlock.questions import Label

from .utils import clear_users

PASSWORD = "password"
PASSWORD_INPUT_HASH = "password_input_hash"
LOGIN_RULE = "/admin-login"
LOGOUT_RULE = "/admin-logout"
DOWNLOAD_RULE = "/admin-download"
STATUS_RULE = "/admin-status"


@pytest.fixture
def login_client():
    class TestConfig(Config):
        PASSWORD = PASSWORD

    app = create_test_app(TestConfig())
    with app.test_client() as client:
        yield client


@pytest.fixture
def client():
    def seed():
        return Page()

    app = create_test_app()
    User.make_test_user(seed).test_get()
    with app.test_client() as client:
        yield client
    clear_users()


class TestLogin:
    enter_password = b"Enter your password."
    incorrect_password = b"Incorrect password."
    password_required = b"Password required."

    def test_login_page(self, login_client):
        response = login_client.get(LOGIN_RULE)
        assert self.enter_password in response.data
        assert self.incorrect_password not in response.data
        assert self.password_required not in response.data

    def test_requested_url(self, login_client):
        response = login_client.get(STATUS_RULE, follow_redirects=True)
        assert self.enter_password in response.data
        assert self.incorrect_password not in response.data
        assert self.password_required in response.data

    def test_correct_password(self, login_client):
        login_client.get(LOGIN_RULE)
        response = login_client.post(LOGIN_RULE, data={PASSWORD_INPUT_HASH: PASSWORD})
        assert password_is_correct()
        bytes(f'href="{STATUS_RULE}"', "utf-8") in response.data

    def test_incorrect_password(self, login_client):
        login_client.get(LOGIN_RULE)
        response = login_client.post(
            LOGIN_RULE, data={PASSWORD_INPUT_HASH: "incorrect_password"}, follow_redirects=True
        )
        assert not password_is_correct()
        assert self.enter_password in response.data
        assert self.incorrect_password in response.data
        assert self.password_required not in response.data


def test_logout(login_client):
    login_client.get(LOGIN_RULE)
    login_client.post(LOGIN_RULE, data={PASSWORD_INPUT_HASH: PASSWORD})
    assert password_is_correct()
    response = login_client.get(LOGOUT_RULE)
    assert not password_is_correct()
    assert bytes(f'href="{LOGIN_RULE}"', "utf-8") in response.data


def test_download(client):
    response = client.get(DOWNLOAD_RULE)
    df = pd.read_csv(io.StringIO(str(response.data, "utf-8")))
    assert len(df) == 1
    assert df.completed.all()


class TestStatus:
    @pytest.mark.parametrize("in_gitpod", (True, False))
    def test_request(self, client, in_gitpod):
        if in_gitpod:
            os.environ["GITPOD_HOST"] = "host"

        clear_users()
        response = client.get(STATUS_RULE)
        if "GITPOD_HOST" in os.environ:
            os.environ.pop("GITPOD_HOST")

        assert b"No users yet." in response.data

    @pytest.mark.parametrize("with_users", (True, False))
    def test_get_user_status(self, with_users):
        if with_users:
            User.make_test_user()
        else:
            clear_users()

        get_user_status(label := Label())
        if with_users:
            assert "Count" in label.label
        else:
            assert label.label is None
