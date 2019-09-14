"""Application factory"""

from hemlock.app.config import Config

# from hemlock.extensions import Compiler, Viewer, AttrSettor
from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash
import pandas as pd
import os

default_settings = {
    'password': '',
    'record_incomplete': True,
    'block_duplicate_ips': False,
    'screenouts_folder': None,
    'static_folder': 'static',
    'css': ['bootstrap.min.css', 'default.min.css'],
    'js': ['default.min.js']
    }

# Create extensions
# compiler = Compiler()
# viewer = Viewer()
# attr_settor = AttrSettor()
bootstrap = Bootstrap()
bp = Blueprint('hemlock', __name__)
db = SQLAlchemy()
# login = LoginManager()
# login.login_view = 'hemlock.index'

'''
Application factory

Arguments:
    config_class: configures application by object
    start: starting navigation function in survey
    password: password for accessing researcher urls
    record_incomplete: indicates incomplete responses should be recorded
    block_duplicates: indicates duplicate IP addresses should be blocked
    block_from_csv: csv file containing IP addresses to block
    static_folder: folder in which statics are stored
'''
def create_app(settings):
    settings, static_folder = merge_with_default(settings)
    app = Flask(__name__, static_folder=static_folder)
    [setattr(app, key, value) for key, value in settings.items()]
    app.password_hash = generate_password_hash(app.password)
    app.config.from_object(Config)
    
    # initialize application features
    # compiler.init_app(app)
    # viewer.init_app(app)
    # attr_settor.init_app(app)
    bootstrap.init_app(app)
    app.register_blueprint(bp)
    db.init_app(app)
    # login.init_app(app)
    
    return app

def merge_with_default(settings):
    for key, value in default_settings.items():
        if key not in settings:
            settings[key] = value
    static_folder = os.path.join(os.getcwd(), settings['static_folder'])
    settings.pop('static_folder')
    return settings, static_folder