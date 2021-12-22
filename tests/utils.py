import pytest
from flask_login import current_user

from hemlock import User, create_test_app
from hemlock.app import db


def clear_users():
    for user in User.query.all():
        db.session.delete(user)
    db.session.commit()

def clear_routes():
    User._seed_funcs.clear()
    User.default_url_rule = None


def make_post_data(direction="forward"):
    return {"direction": direction, "page-hash": current_user.get_tree().page.hash}


@pytest.fixture
def app():
    yield create_test_app()
    clear_users()


@pytest.fixture
def client():
    app = create_test_app()
    with app.test_client() as client:
        yield client
    clear_users()
