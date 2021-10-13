import pytest

from hemlock import User, Page, create_test_app
from hemlock.app import Config
from hemlock.questions import Label

STUDY_RULE = "/test_route_url_rule"
ERROR_RULE = "/test_error_url_rule"
SCREENOUT_RULE = "/screenout"
RESTART_RULE = "/restart"

ZEROETH_PAGE_LABEL = "page 0"
FIRST_PAGE_LABEL = "page 1"


@User.route(STUDY_RULE)
def seed():
    return [Page(Label(ZEROETH_PAGE_LABEL)), Page(Label(FIRST_PAGE_LABEL))]


class TestIndex:
    def test_new_user(self):
        app = create_test_app()
        with app.test_client() as client:
            response = client.get("/")
        assert bytes(f'href="{STUDY_RULE}"', "utf-8") in response.data

    def test_restart_on_first_page(self):
        # client should be taken back to the first page if he attempts to restart
        # while still on the first page
        app = create_test_app()
        with app.test_client() as client:
            client.get("/", follow_redirects=True)
            response = client.get("/")
        assert bytes(f'href="{STUDY_RULE}"', "utf-8") in response.data

    def test_screenout(self):
        key, value = "key", "value"
        config = Config()
        config.SCREENOUT_RECORDS = {key: [value]}
        app = create_test_app(config)
        with app.test_client() as client:
            response = client.get("/", query_string={key: value})
        assert bytes(f'href="{SCREENOUT_RULE}"', "utf-8") in response.data

    @pytest.mark.parametrize("allow_users_to_restart", (True, False))
    def test_restart(self, allow_users_to_restart):
        config = Config()
        config.ALLOW_USERS_TO_RESTART = allow_users_to_restart
        app = create_test_app(config)
        with app.test_client() as client:
            client.get("/")
            client.post(STUDY_RULE, data={"direction": "forward"})
            response = client.get("/")
        expected_rule = RESTART_RULE if allow_users_to_restart else STUDY_RULE
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
        assert bytes(f'href="{expected_rule}"', "utf-8") in response.data


def test_screenout():
    app = create_test_app()
    with app.test_client() as client:
        response = client.get(SCREENOUT_RULE)
    assert response.status == "200 OK"


class TestRestart:
    @staticmethod
    def get_restart_response(client):
        client.get("/")
        client.post(STUDY_RULE, data={"direction": "forward"})
        return client.get(RESTART_RULE)

    def test_get(self):
        app = create_test_app()
        with app.test_client() as client:
            response = self.get_restart_response(client)
        assert response.status == "200 OK"

    @pytest.mark.parametrize("resume", (True, False))
    def test_post(self, resume):
        direction = "back" if resume else "forward"
        app = create_test_app()
        with app.test_client() as client:
            self.get_restart_response(client)
            response = client.post(
                RESTART_RULE, data={"direction": direction}, follow_redirects=True
            )
        # client should be on the first page if he chose to resume
        # and the zeroeth page if he chose to restart
        expected_label = FIRST_PAGE_LABEL if resume else ZEROETH_PAGE_LABEL
        assert bytes(expected_label, "utf-8") in response.data


@User.route(ERROR_RULE)
def error_seed():
    return Page(compile=divide_by_0)


def divide_by_0(page):
    x = 1 / 0


def test():
    app = create_test_app()
    with app.test_client() as client:
        client.get("/")
        response = client.get(ERROR_RULE)
    assert response.status == "500 INTERNAL SERVER ERROR"
    assert b"The application encountered an error" in response.data
