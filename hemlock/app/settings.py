"""Application default settings and configuration object

time_limit and status_logger_period must be in 'hh:mm:ss' format.
"""

from hemlock.app.setting_utils import *

from datetime import datetime, timedelta
from glob import glob
from werkzeug.security import generate_password_hash
import os
import pandas as pd

default_settings = {
    'back': False,
    'back_button': BACK_BUTTON,
    'duplicate_keys': ['IPv4', 'workerId'],
    'css': ['css/bootstrap.min.css', 'css/default.min.css'],
    'forward_button': FORWARD_BUTTON,
    'js': 'js/default.min.js',
    'page_compile': page_compile,
    'page_debug': None,
    'page_post': page_post,
    'password': '',
    'question_compile': None,
    'question_debug': None,
    'question_interval': None,
    'question_post': None,
    'restart_option': True,
    'restart_text': RESTART,
    'screenout_folder': 'screenouts',
    'screenout_keys': ['IPv4', 'workerId'],
    'screenout_text': SCREENOUT,
    'socket_js': '//cdnjs.cloudflare.com/ajax/libs/socket.io/1.3.6/socket.io.min.js',
    'static_folder': 'static',
    'status_log_period': '00:02:00',
    'survey_template': 'default_survey.html',
    'template_folder': 'templates',
    'time_expired_text': TIME_EXPIRED,
    'time_limit': None,
    'view_template': 'default_view.html'
    }
    
def get_settings(settings):
    """Get application settings
    
    Overwrite default settings with input settings. Convert settings to list 
    and timedelta objects as needed.
    
    Then merge static and template folders with current working directory. 
    Return these separately, as they need to be passed to the Flask 
    constructor.
    """
    settings = settings.copy()
    for key, value in default_settings.items():
        if key not in settings:
            settings[key] = value
    to_list(settings, 'duplicate_keys')
    to_list(settings, 'css')
    to_list(settings, 'js')
    to_list(settings, 'screenout_keys')
    to_timedelta(settings, 'time_limit')
    to_timedelta(settings, 'status_log_period')
    settings['password_hash'] = generate_password_hash(
        settings.pop('password'))
    cwd = os.getcwd()
    static = os.path.join(cwd, settings.pop('static_folder'))
    templates = os.path.join(cwd, settings.pop('template_folder'))
    return settings, static, templates
    
def to_list(settings, key):
    """Convert setting item to list"""
    item = settings[key]
    if item is None:
        settings[key] = []
    if isinstance(item, str):
        settings[key] = [item]

def to_timedelta(settings, key):
    """Convert time expressed as 'hh:mm:ss' to timedelta object"""
    time_str = settings[key]
    if time_str is None:
        return
    t = datetime.strptime(time_str, '%H:%M:%S')
    settings[key] = timedelta(hours=t.hour,minutes=t.minute,seconds=t.second)

def get_screenouts(app):
    """Store screenouts dictionary as application attribute"""
    app.screenout_folder = os.path.join(os.getcwd(), app.screenout_folder)
    screenout_csvs = glob(app.screenout_folder+'/*.csv')
    df = pd.concat([pd.read_csv(csv) for csv in screenout_csvs]).astype(str)
    app.screenouts = df.to_dict(orient='list')

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') 
        or 'sqlite:///'+os.path.join(os.getcwd(), 'data.db')
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WKHTMLTOIMAGE = os.environ.get('WKHTMLTOIMAGE')
    