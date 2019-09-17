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
    
    Overwrite default settings with input settings. Then merge static and 
    template folders with current working directory. Return these separately,
    as they need to be passed to the Flask constructor.
    """
    for key, value in default_settings.items():
        if key not in settings:
            settings[key] = value
    if settings['time_limit'] is not None:
        t = datetime.strptime(settings['time_limit'], '%H:%M:%S')
        settings['time_limit'] = timedelta(
            hours=t.hour, minutes=t.minute, seconds=t.second)
    settings['password_hash'] = generate_password_hash(
        settings.pop('password'))
    cwd = os.getcwd()
    static = os.path.join(cwd, settings.pop('static_folder'))
    templates = os.path.join(cwd, settings.pop('template_folder'))
    return settings, static, templates

def get_screenouts(app):
    """Store screenouts dictionary as application attribute"""
    app.screenouts_folder = os.path.join(os.getcwd(), app.screenouts_folder)
    screenout_csvs = glob(app.screenouts_folder+'/*.csv')
    df = pd.concat([pd.read_csv(csv) for csv in screenout_csvs]).astype(str)
    app.screenouts = df.to_dict(orient='list')