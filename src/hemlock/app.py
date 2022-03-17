"""Application utilities.
"""
from __future__ import annotations

import os
from collections import defaultdict
from typing import Any, Dict, List, Mapping, Union

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
Mutable.set_session(db.session)

login_manager = LoginManager()
login_manager.login_view = "hemlock.index"
login_manager.login_message = None

socketio = SocketIO()

# for caching static pages
static_pages: Dict[str, str] = {}


class Config:
    """Default configuration file."""

    ALLOW_USERS_TO_RESTART: bool = True
    SCREENOUT_RECORDS: Dict[str, List[str]] = {}
    BLOCK_DUPLICATE_KEYS: List[str] = []
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    USER_METADATA: defaultdict[str, List[str]] = defaultdict(list)

    @property
    def PASSWORD(self) -> str:
        return os.getenv("PASSWORD", "")

    @property
    def PASSWORD_HASH(self) -> str:
        if not hasattr(self, "_PASSWORD_HASH"):
            self._PASSWORD_HASH = generate_password_hash(self.PASSWORD)
        return self._PASSWORD_HASH

    @property
    def SECRET_KEY(self) -> str:
        return os.getenv("SECRET_KEY", "secret")

    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        uri = os.getenv("DATABASE_URL", "sqlite://")
        if uri.startswith("postgres://"):
            # see https://help.heroku.com/ZKNTJQSK/why-is-sqlalchemy-1-4-x-not-connecting-to-heroku-postgres
            return uri.replace("postgres://", "postgresql://", 1)

        return uri

    @property
    def SQLALCHEMY_ENGINE_OPTIONS(self) -> Dict[str, Any]:
        if self.SQLALCHEMY_DATABASE_URI.startswith("sqlite"):
            return {}

        return {"pool_size": 1, "pool_recycle": 10, "max_overflow": 0}


@bp.before_app_first_request
def init_app() -> None:
    """Create database."""
    db.create_all()


def create_app(
    *config: Union[Mapping, Config],
    static_folder: str = None,
    template_folder: str = None,
    **kwargs: Any,
) -> Flask:
    """Create application.

    See :class:`hemlock.app.Config` for default configuration.

    Args:
        *config (Union[Mapping, Config]): Configuration objects. Defaults to None.
        static_folder (str, optional): Static folder argument for ``flask.Flask``.
        template_folder (str, optional): Template folder argument for ``flask.Flask``.
        **kwargs (Any): Passed to ``flask.Flask``.

    Returns:
        Flask: Application.
    """
    if static_folder is None:
        static_folder = os.path.join(os.getcwd(), "static")

    if template_folder is None:
        template_folder = os.path.join(os.getcwd(), "templates")

    app = Flask(
        __name__, static_folder=static_folder, template_folder=template_folder, **kwargs
    )

    # set up configuration
    for item in config or (Config(),):
        if isinstance(item, Mapping):
            app.config.update(item)
        else:
            app.config.from_object(item)

    app.register_blueprint(bp)

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    return app


def create_test_app(*args: Any, **kwargs: Any) -> Flask:
    """Create a test application.

    Arguments and keywords arguments passed to :func:`hemlock.app.create_app`.

    Returns:
        Flask: Test application.
    """
    app = create_app(*args, **kwargs)
    app.config["TESTING"] = True
    app.app_context().push()
    init_app()

    return app
