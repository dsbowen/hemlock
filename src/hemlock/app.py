"""Application utilities.
"""
from __future__ import annotations

import os
from collections import defaultdict
from typing import Any, Dict

from flask import Blueprint, Flask
from flask_login import LoginManager
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_mutable import Mutable
from werkzeug.security import generate_password_hash

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
sqlalchemy_database_uri = os.environ.get("DATABASE_URL", "sqlite://")
if sqlalchemy_database_uri.startswith("postgres://"):
    # see https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
    sqlalchemy_database_uri = sqlalchemy_database_uri.replace("postgres://", "postgresql://", 1)
settings = {
    "allow_users_to_restart": True,
    "screenout_records": {},
    "block_duplicate_keys": [],
    "static_folder": "static",
    "template_folder": os.path.join(os.getcwd(), "templates"),
    "config": {
        "PASSWORD": os.environ.get("PASSWORD", ""),
        "SECRET_KEY": os.environ.get("SECRET_KEY", "secret"),
        "SQLALCHEMY_DATABASE_URI": sqlalchemy_database_uri,
        "SQLALCHEMY_TRACK_MODIFICATIONS": False,
        "SQLALCHEMY_ENGINE_OPTIONS": (
            {}
            if sqlalchemy_database_uri.startswith("sqlite")
            else dict(pool_size=1, pool_recycle=10, max_overflow=0)
        ),
    },
}

# for caching static pages
static_pages = {}


@bp.before_app_first_request
def init_app() -> None:
    """Create database."""
    db.create_all()


def create_app(settings: Dict[Any, Any] = settings) -> Flask:
    """Create application.

    Args:
        settings (Dict[Any, Any], optional): Applciation settings. Defaults to settings.

    Returns:
        Flask: Application.
    """
    app = Flask(
        __name__,
        static_folder=settings["static_folder"],
        template_folder=settings["template_folder"],
    )

    settings["config"]["PASSWORD_HASH"] = generate_password_hash(
        settings["config"].get("PASSWORD", "")
    )
    app.config.update(settings["config"])
    app.settings = settings  # type: ignore
    app.user_metadata = defaultdict(list)  # type: ignore
    app.register_blueprint(bp)

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    return app


def create_test_app(settings: Dict[Any, Any] = settings) -> Flask:
    """Create a test application.

    Args:
        settings (Dict[Any, Any], optional): Application settings. Defaults to settings.

    Returns:
        Flask: Test application.
    """
    app = create_app(settings)
    app.app_context().push()
    init_app()

    return app
