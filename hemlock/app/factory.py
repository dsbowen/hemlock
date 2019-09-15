"""Application factory"""

from hemlock.app.config import Config
# from hemlock.extensions import Viewer

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash
import pandas as pd
import os

default_settings = {
    'block_duplicate_ips': False,
    'css': ['css/bootstrap.min.css', 'css/default.min.css'],
    'js': ['js/default.min.js'],
    'password': '',
    'record_incomplete': True,
    'screenouts_folder': None,
    'static_folder': 'static',
    'survey_template': 'default_survey.html',
    'template_folder': 'templates',
    'view_template': 'default_view.html'
    }

"""Flask and Hemlock extensions"""
bootstrap = Bootstrap()
bp = Blueprint('hemlock', __name__)
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'hemlock.index'
# viewer = Viewer()


def create_app(settings):
    """Application factory
    
    Begins with settings and configuration. Then registers blueprint and 
    extensions.
    """
    settings, static, templates = get_settings(settings)
    app = Flask(__name__, static_folder=static, template_folder=templates)
    [setattr(app, key, value) for key, value in settings.items()]
    app.password_hash = generate_password_hash(app.password)
    app.config.from_object(Config)
    
    bootstrap.init_app(app)
    app.register_blueprint(bp)
    db.init_app(app)
    login_manager.init_app(app)
    # viewer.init_app(app)
    
    return app

def get_settings(settings):
    """Get application settings
    
    Overwrite default settings with input settings. Then merge static and 
    template folders with current working directory. Return these separately,
    as they need to be passed to the Flask constructor.
    """
    for key, value in default_settings.items():
        if key not in settings:
            settings[key] = value
    cwd = os.getcwd()
    static = os.path.join(cwd, settings.pop('static_folder'))
    templates = os.path.join(cwd, settings.pop('template_folder'))
    return settings, static, templates