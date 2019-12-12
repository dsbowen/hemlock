"""Application default settings and configuration object

time_limit and status_logger_period must be in 'hh:mm:ss' format.
"""

from hemlock.app.settings_utils import *

from datetime import datetime, timedelta
from flask import Markup
from glob import glob
from werkzeug.security import generate_password_hash
import os
import pandas as pd

default_settings = {
    'clean_data': clean_data,
    'duplicate_keys': ['IPv4', 'workerId'],
    'offline': False,
    'password': '',
    'restart_option': True,
    'restart_text': RESTART,
    'screenout_folder': 'screenouts',
    'screenout_keys': ['IPv4', 'workerId'],
    'screenout_text': SCREENOUT,
    'socket_js': SOCKET_JS,
    'static_folder': 'static',
    'status_log_period': '00:02:00',
    'template_folder': 'templates',
    'time_expired_text': TIME_EXPIRED,
    'time_limit': None,
    'download_btn_settings': {
        'btn_classes': ['btn', 'btn-outline-primary', 'w-100'],
    },
    'manager_settings': {
        'blueprint': 'hemlock'
    },
    'page_settings': {
        'back': False,
        'back_button': BACK_BUTTON,
        'compile_functions': compile_function,
        'css': PAGE_CSS,
        'debug_functions': debug_function,
        'forward': True,
        'forward_button': FORWARD_BUTTON,
        'js': PAGE_JS,
        'submit_functions': submit_function,
        'template': 'default.html',
        'validate_functions': validate_function,
    },
    'question_settings': {
        'div_classes': ['form-group', 'question'],
        'css': [],
        'js': [],
    },
    'single_choice_settings': {
        'choice_div_classes': ['custom-control', 'custom-radio'],
        'choice_input_type': 'radio',
    },
    'multi_choice_settings': {
        'choice_div_classes': ['custom-control', 'custom-checkbox'],
        'choice_input_type': 'checkbox',
    },
}
    
def get_settings(settings):
    """Get application settings
    
    Overwrite default settings with input settings. Convert settings to list 
    and timedelta objects as needed.
    
    Then merge static and template folders with current working directory. 
    Return these separately, as they need to be passed to the Flask 
    constructor.
    """
    override_default_settings(settings, default_settings)

    to_timedelta(settings, 'time_limit')
    to_timedelta(settings, 'status_log_period')

    page_settings = settings['page_settings']
    to_Markup(page_settings, 'back_button')
    to_Markup(page_settings, 'forward_button')

    password = settings.pop('password')
    settings['password_hash'] = generate_password_hash(password)
    cwd = os.getcwd()
    static = os.path.join(cwd, settings.pop('static_folder'))
    templates = os.path.join(cwd, settings.pop('template_folder'))
    return settings, static, templates

def override_default_settings(settings, default_settings):
    """Recursively override default settings"""
    for key, value in default_settings.items():
        if key not in settings:
            settings[key] = value
        elif isinstance(settings[key], dict):
            override_default_settings(settings[key], value)

def to_Markup(settings, key):
    """Convert setting item to Markup"""
    item = settings[key]
    if not isinstance(item, Markup):
        settings[key] = Markup(item)

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
    """Application configuration object"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') 
        or 'sqlite:///'+os.path.join(os.getcwd(), 'data.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'