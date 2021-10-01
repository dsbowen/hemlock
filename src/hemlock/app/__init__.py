import os
from collections import defaultdict

from flask import Blueprint, Flask, current_app
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_mutable import Mutable
from werkzeug.security import generate_password_hash

from ._make_static_pages import (
    make_loading_page,
    make_restart_page,
    make_screenout_page,
    make_500_page,
)

# create blueprint and extensions
bp = Blueprint(
    "hemlock",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/hemlock/static",
)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "hemlock.index"
login_manager.login_message = None
socketio = SocketIO()
Mutable.set_session(db.session)

# create default settings
password = os.environ.get("PASSWORD", "")
sqlalchemy_database_uri = os.environ.get(
    "DATABASE_URL", f"sqlite:///{os.path.join(os.getcwd(), 'data.db')}"
)
settings = {
    "loading_page": make_loading_page,
    "restart_page": make_restart_page,
    "allow_users_to_restart": os.environ.get("ALLOW_USERS_TO_RESTART", "true").lower()
    == "true",
    "screenout_page": make_screenout_page,
    "screenout_records": {},
    "block_duplicate_keys": [],
    "internal_server_error_page": make_500_page,
    "static_folder": "static",
    "template_folder": os.path.join(os.getcwd(), "templates"),
    "config": {
        "PASSWORD": password,
        "PASSWORD_HASH": generate_password_hash(password),
        "SECRET_KEY": os.environ.get("SECRET_KEY", "secret"),
        "SQLALCHEMY_DATABASE_URI": sqlalchemy_database_uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_ENGINE_OPTIONS": dict(
            {}
            if sqlalchemy_database_uri.startswith("sqlite")
            else dict(pool_size=1, pool_recycle=10, max_overflow=0)
        ),
    },
}


@bp.before_app_first_request
def init_app():
    db.create_all()
    static_pages = [
        "loading_page",
        "restart_page",
        "screenout_page",
        "internal_server_error_page",
    ]
    for key in static_pages:
        page = current_app.settings[key]
        if callable(page):
            current_app.settings[key] = page()


def create_app(settings=settings):
    app = Flask(
        __name__,
        static_folder=settings["static_folder"],
        template_folder=settings["template_folder"],
    )

    app.config.update(settings["config"])
    app.settings = settings
    app.user_metadata = defaultdict(list)
    app.register_blueprint(bp)

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    return app


def create_test_app(use_in_memory_database=True, settings=settings):
    if use_in_memory_database:
        settings["config"]["SQLALCHEMY_DATABASE_URI"] = "sqlite://"

    app = create_app()
    app.app_context().push()
    db.create_all()

    return app
