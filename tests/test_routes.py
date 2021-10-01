import pytest

from hemlock import User, Page
from hemlock.app import create_test_app, settings
from hemlock.questions import Label

STUDY_RULE = "/test_route_url_rule"
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
        settings["screenout_records"] = {key: [value]}
        app = create_test_app()
        with app.test_client() as client:
            response = client.get("/", query_string={key: value})
        settings["screenout_records"].clear()
        assert bytes(f'href="{SCREENOUT_RULE}"', "utf-8") in response.data

    @pytest.mark.parametrize("allow_users_to_restart", (True, False))
    def test_restart(self, allow_users_to_restart):
        settings["allow_users_to_restart"] = allow_users_to_restart
        app = create_test_app()
        with app.test_client() as client:
            client.get("/")
            client.post(STUDY_RULE, data={"direction": "forward"})
            response = client.get("/")
        settings["allow_users_to_restart"] = True
        expected_rule = RESTART_RULE if allow_users_to_restart else STUDY_RULE
        assert bytes(f'href="{expected_rule}"', "utf-8") in response.data

    @pytest.mark.parametrize("block_duplicates", (True, False))
    def test_duplicate(self, block_duplicates):
        query_string = {"key": "value"}

        if block_duplicates:
            settings["block_duplicate_keys"] = query_string.keys()
        else:
            settings["block_duplicate_keys"] = []

        app = create_test_app()
        with app.test_client() as client:
            client.get("/", query_string=query_string)

        with app.test_client() as client:
            response = client.get("/", query_string=query_string)

        settings["block_duplicate_keys"] = []
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
