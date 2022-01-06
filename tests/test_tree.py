import pytest

from hemlock import Tree, Page
from hemlock.app import create_test_app, static_pages

from .utils import app


def seed():
    return [Page(), Page()]


def make_post_data(tree, direction="forward"):
    return {"direction": direction, "page-hash": tree.page.hash}


def test_custom_url_rule():
    url_rule = "/custom_rule"
    assert Tree(seed, url_rule=url_rule).url_rule == url_rule


def test_repr():
    tree = Tree(seed)
    repr_tree = repr(tree)
    assert repr_tree.startswith("<Tree id: None")
    for page in tree.branch:
        assert str(page) in repr_tree


class TestNavigation:
    def test_back_error(self):
        # test that you cannot go back from the first page
        tree = Tree(seed)
        with pytest.raises(RuntimeError):
            tree.go_back()

    def test_forward_error(self):
        # test that you cannot go forward from the last page
        tree = Tree(seed)
        tree.go_forward()
        with pytest.raises(RuntimeError):
            tree.go_forward()

    def test_easy_navigation(self):
        def seed():
            branch = [
                Page(),
                first_page := Page(),
                Page(back=True),
                Page(back=True, prev_page=first_page),
            ]
            branch[0].next_page = branch[2]
            return branch

        tree = Tree(seed)
        assert tree.page.get_position() == "0"
        assert tree.go_forward().page.get_position() == "2"
        assert tree.go_forward().page.get_position() == "3"
        assert tree.go_back().page.get_position() == "1"
        assert tree.go_forward().page.get_position() == "2"
        assert tree.go_back().page.get_position() == "1"

    def test_hard_navigation(self):
        def seed():
            branch = [Page(), Page()]

            first_branch = [Page(), Page()]
            branch[0].branch = first_branch

            first_branch[0].branch = [Page(next_page=branch[1])]
            first_branch[1].branch = [Page()]

            branch[1].prev_page = first_branch[1]

            return branch

        tree = Tree(seed)
        assert tree.page.get_position() == "0"

        assert tree.go_forward().page.get_position() == "0.0"
        assert tree.go_back().page.get_position() == "0"
        assert tree.go_forward().page.get_position() == "0.0"

        assert tree.go_forward().page.get_position() == "0.0.0"
        assert tree.go_back().page.get_position() == "0.0"
        assert tree.go_forward().page.get_position() == "0.0.0"

        assert tree.go_forward().page.get_position() == "1"
        assert tree.go_back().page.get_position() == "0.1"
        assert tree.go_back().page.get_position() == "0.0.0"
        assert tree.go_forward().page.get_position() == "1"

        assert tree.go_back().page.get_position() == "0.1"
        assert tree.go_forward().page.get_position() == "0.1.0"
        assert tree.go_back().page.get_position() == "0.1"

        assert tree.go_forward().page.get_position() == "0.1.0"
        assert tree.go_forward().page.get_position() == "1"


class TestProcessRequest:
    def test_request_in_progress(self, app):
        # should return a loading page if the tree is already processing a request
        tree = Tree(seed)
        tree.request_in_progress = True
        with app.test_request_context():
            rv = tree.process_request()
        assert rv == static_pages["loading_page"]

    def test_double_post(self, app):
        # should return loading page after two consecutive POST requests
        tree = Tree(seed, url_rule="/survey")
        tree.prev_request_method = "POST"
        tree.request_in_progress = False
        with app.test_request_context(method="POST", data=make_post_data(tree)):
            rv = tree.process_request()
        assert rv == static_pages["loading_page"]

    def test_stale_post(self, app):
        # should return the cached page after stale POST request
        # the request is "stale" in the sense that it was issued on the previous page
        # e.g., a user submits 2 POST requests from the same page, the first POST
        # request redirects with a GET request, then the second POST request is
        # processed
        tree = Tree(seed, url_rule="/survey")
        with app.test_request_context():
            tree.process_request()
        with app.test_request_context(method="POST", data=make_post_data(tree)):
            tree.process_request()
        with app.test_request_context():
            tree.process_request()
        with app.test_request_context(
            method="POST",
            data={"direction": "forward", "page-hash": tree.branch[0].hash},
        ):
            rv = tree.process_request()
        assert rv == tree.cached_page_html

    def test_refresh(self, app):
        # should return the current page on refresh
        tree = Tree(seed)
        with app.test_request_context():
            tree.process_request()
        with app.test_request_context():
            rv = tree.process_request()
        assert rv == tree.cached_page_html

    def test_post(self, app):
        tree = Tree(seed, url_rule="/survey")
        assert tree.page is tree.branch[0]

        with app.test_request_context(method="POST", data=make_post_data(tree)):
            tree.process_request()
        assert tree.page is tree.branch[1]

        with app.test_request_context():
            tree.process_request()

        with app.test_request_context(method="POST", data=make_post_data(tree, "back")):
            tree.process_request()
        assert tree.page is tree.branch[0]
