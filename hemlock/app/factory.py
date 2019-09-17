"""Application factory"""

from hemlock.app.settings import get_settings, get_screenouts, Config
# from hemlock.extensions import Viewer

from datetime import datetime, timedelta
from flask import Flask, Blueprint
from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

"""Flask and Hemlock extensions"""
bootstrap = Bootstrap()
bp = Blueprint('hemlock', __name__)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'hemlock.index'
login_manager.login_message = None
scheduler = APScheduler()
# viewer = Viewer()


def create_app(settings):
    """Application factory
    
    Begins with settings and configuration. Then registers blueprint and 
    extensions.
    """
    settings, static, templates = get_settings(settings)
    app = Flask(__name__, static_folder=static, template_folder=templates)
    [setattr(app, key, value) for key, value in settings.items()]
    app.status_tracker = {'completed': 0, 'in progress': 0, 'timed out': 0}
    app.config.from_object(Config)
    
    get_screenouts(app)
    
    bootstrap.init_app(app)
    app.register_blueprint(bp)
    db.init_app(app)
    login_manager.init_app(app)
    scheduler.init_app(app)
    scheduler.start()
    # viewer.init_app(app)
    
    return app