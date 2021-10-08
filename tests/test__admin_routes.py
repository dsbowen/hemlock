import pytest

from hemlock import User, create_test_app
from hemlock._admin_routes import password_is_correct, get_user_status
from hemlock.app import db, settings
from hemlock.questions import Label

PASSWORD = "password"
LOGIN_RULE = "/admin-login"
LOGOUT_RULE = "/admin-logout"
STATUS_RULE = "/admin-status"


@pytest.fixture
def login_client():
    settings["config"]["PASSWORD"] = PASSWORD
    app = create_test_app()
    with app.test_client() as client:
        yield client
    settings["config"]["PASSWORD"] = ""


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
        response = login_client.post(LOGIN_RULE, data={"input_hash": PASSWORD})
        assert password_is_correct()
        bytes(f'href="{STATUS_RULE}"', "utf-8") in response.data

    def test_incorrect_password(self, login_client):
        login_client.get(LOGIN_RULE)
        response = login_client.post(
            LOGIN_RULE, data={"input_hash": "incorrect_password"}, follow_redirects=True
        )
        assert not password_is_correct()
        assert self.enter_password in response.data
        assert self.incorrect_password in response.data
        assert self.password_required not in response.data


def test_logout(login_client):
    login_client.get(LOGIN_RULE)
    login_client.post(LOGIN_RULE, data={"hash": PASSWORD})
    assert password_is_correct()
    response = login_client.get(LOGOUT_RULE)
    assert not password_is_correct()
    assert bytes(f'href="{LOGIN_RULE}"', "utf-8") in response.data


class TestStatus:
    def test_request(self):
        app = create_test_app()
        with app.test_client() as client:
            response = client.get(STATUS_RULE)
        assert b"No users yet." in response.data

    @pytest.mark.parametrize("with_users", (True, False))
    def test_get_user_status(self, with_users):
        if with_users:
            User.make_test_user()
        else:
            [db.session.delete(user) for user in User.query.all()]
            db.session.commit()

        get_user_status(label := Label())
        if with_users:
            assert "Count" in label.label
        else:
            assert label.label is None
