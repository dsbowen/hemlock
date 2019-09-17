"""Application factory"""

from hemlock.app.settings import default_settings, Config
# from hemlock.extensions import Viewer

from datetime import datetime, timedelta
from flask import Flask, Blueprint
from flask_apscheduler import APScheduler
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from glob import glob
from werkzeug.security import generate_password_hash
import pandas as pd
import os

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

def get_settings(settings):
    """Get application settings
    
    Overwrite default settings with input settings. 
    
    Convert time limit to timedelta object. Convert screenout keys, css, and 
    js to lists.
    
    Then merge static and template folders with current working directory. 
    Return these separately, as they need to be passed to the Flask 
    constructor.
    """
    settings = settings.copy()
    for key, value in default_settings.items():
        if key not in settings:
            settings[key] = value
    if settings['time_limit'] is not None:
        t = datetime.strptime(settings['time_limit'], '%H:%M:%S')
        settings['time_limit'] = timedelta(
            hours=t.hour, minutes=t.minute, seconds=t.second)
    if settings['duplicate_keys'] is None:
        settings['duplicate_keys'] = []
    if isinstance(settings['css'], str):
        settings['css'] = [settings['css']]
    if isinstance(settings['js'], str):
        settings['js'] = [settings['js']]
    if settings['screenout_keys'] is None:
        settings['screenout_keys'] = []
    settings['password_hash'] = generate_password_hash(
        settings.pop('password'))
    cwd = os.getcwd()
    static = os.path.join(cwd, settings.pop('static_folder'))
    templates = os.path.join(cwd, settings.pop('template_folder'))
    return settings, static, templates

def get_screenouts(app):
    """Store screenouts dictionary as application attribute"""
    app.screenout_folder = os.path.join(os.getcwd(), app.screenout_folder)
    screenout_csvs = glob(app.screenout_folder+'/*.csv')
    df = pd.concat([pd.read_csv(csv) for csv in screenout_csvs]).astype(str)
    app.screenouts = df.to_dict(orient='list')