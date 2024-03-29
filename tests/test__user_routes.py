import pytest

from flask_login import current_user
from hemlock import User, Page, create_test_app
from hemlock._user_routes import internal_server_error
from hemlock.app import Config
from hemlock.questions import Label

from .utils import app, client, clear_users, make_post_data

STUDY_RULE = "/test_route_url_rule"
SCREENOUT_RULE = "/screenout"
RESTART_RULE = "/restart"

ZEROETH_PAGE_LABEL = "page 0"
FIRST_PAGE_LABEL = "page 1"


@User.route(STUDY_RULE)
def seed():
    return [Page(Label(ZEROETH_PAGE_LABEL)), Page(Label(FIRST_PAGE_LABEL))]


class TestIndex:
    def test_new_user(self, client):
        assert bytes(f'href="{STUDY_RULE}"', "utf-8") in client.get("/").data

    @pytest.mark.parametrize("route", ("/", STUDY_RULE))
    def test_metadata_from_querystring(self, client, route):
        key, value = "key", "value"
        client.get(route, query_string={key: value}, follow_redirects=True)
        assert current_user.get_meta_data()[key] == value

    def test_restart_on_first_page(self, client):
        # client should be taken back to the first page if he attempts to restart
        # while still on the first page
        client.get("/", follow_redirects=True)
        assert bytes(f'href="{STUDY_RULE}"', "utf-8") in client.get("/").data

    def test_screenout(self):
        key, value = "key", "value"
        config = Config()
        config.SCREENOUT_RECORDS = {key: [value]}
        app = create_test_app(config)
        with app.test_client() as client:
            response = client.get("/", query_string={key: value})
        clear_users()
        assert bytes(f'href="{SCREENOUT_RULE}"', "utf-8") in response.data

    @pytest.mark.parametrize("allow_users_to_restart", (True, False))
    def test_restart(self, allow_users_to_restart):
        config = Config()
        config.ALLOW_USERS_TO_RESTART = allow_users_to_restart
        app = create_test_app(config)
        with app.test_client() as client:
            client.get("/")
            client.post(STUDY_RULE, data=make_post_data())
            response = client.get("/")
        expected_rule = RESTART_RULE if allow_users_to_restart else STUDY_RULE
        clear_users()
        assert bytes(f'href="{expected_rule}"', "utf-8") in response.data

    @pytest.mark.parametrize("block_duplicates", (True, False))
    def test_duplicate(self, block_duplicates):
        query_string = {"key": "value"}
        config = Config()
        config.USER_METADATA.clear()
        if block_duplicates:
            config.BLOCK_DUPLICATE_KEYS = query_string.keys()

        app = create_test_app(config)
        with app.test_client() as client:
            client.get("/", query_string=query_string)

        with app.test_client() as client:
            response = client.get("/", query_string=query_string)

        expected_rule = SCREENOUT_RULE if block_duplicates else STUDY_RULE
        clear_users()
        assert bytes(f'href="{expected_rule}"', "utf-8") in response.data


def test_screenout(client):
    assert client.get(SCREENOUT_RULE).status == "200 OK"


class TestRestart:
    @staticmethod
    def get_restart_response(client):
        client.get("/")
        client.post(STUDY_RULE, data=make_post_data())
        return client.get(RESTART_RULE)

    def test_get(self, client):
        assert self.get_restart_response(client).status == "200 OK"

    @pytest.mark.parametrize("resume", (True, False))
    def test_post(self, client, resume):
        direction = "back" if resume else "forward"
        self.get_restart_response(client)
        response = client.post(
            RESTART_RULE, data={"direction": direction}, follow_redirects=True
        )
        # client should be on the first page if he chose to resume
        # and the zeroeth page if he chose to restart
        expected_label = FIRST_PAGE_LABEL if resume else ZEROETH_PAGE_LABEL
        assert bytes(expected_label, "utf-8") in response.data


def test_internal_server_error(app):
    with app.test_request_context():
        response = internal_server_error("error")
        assert current_user.errored
    assert "The application encountered an error" in response[0]
    assert response[1] == 500
