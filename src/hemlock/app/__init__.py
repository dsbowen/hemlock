import os

from flask import Blueprint, Flask, current_app
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
password = os.environ.get("PASSWORD", "")
sqlalchemy_database_uri = os.environ.get(
    "DATABASE_URL", f"sqlite:///{os.path.join(os.getcwd(), 'data.db')}"
)
settings = {
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
def init_blueprint():
    # TODO: cache static pages
    db.create_all()


def create_app(settings=settings):
    app = Flask(
        __name__,
        static_folder=settings.get("static_folder"),
        template_folder=settings.get("template_folder"),
    )

    # TODO get screenouts
    app.config.update(settings.get("config"))
    app.register_blueprint(bp)

    # initialize extensions
    db.init_app(app)
    login_manager.init_app(app)
    socketio.init_app(app)

    return app
