import pytest

from hemlock import Tree, Page
from hemlock.app import create_test_app, static_pages


def seed():
    return [Page(), Page()]


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
    def test_request_in_progress(self):
        # should return a loading page if the tree is already processing a request
        app = create_test_app()
        tree = Tree(seed)
        tree.request_in_progress = True
        with app.test_request_context():
            rv = tree.process_request()
        assert rv == static_pages["loading_page"]

    def test_refresh(self):
        # should return the current page on refresh
        app = create_test_app()
        tree = Tree(seed)
        with app.test_request_context():
            tree.process_request()
        with app.test_request_context():
            rv = tree.process_request()
        assert rv == tree.cached_page_html

    def test_post(self):
        app = create_test_app()
        tree = Tree(seed, url_rule="/survey")
        assert tree.page is tree.branch[0]

        with app.test_request_context(method="POST", data={"direction": "forward"}):
            tree.process_request()
        assert tree.page is tree.branch[1]

        with app.test_request_context(method="POST", data={"direction": "back"}):
            tree.process_request()
        assert tree.page is tree.branch[0]
