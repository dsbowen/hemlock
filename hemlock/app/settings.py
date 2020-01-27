"""Application settings and configuration object

time_limit and status_logger_period must be in 'hh:mm:ss' format.
"""

from datetime import datetime, timedelta
from glob import glob
from werkzeug.security import generate_password_hash
import os
import pandas as pd


class Config():
    """Application configuration object"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') 
        or 'sqlite:///'+os.path.join(os.getcwd(), 'data.db')
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    REDIS_URL = os.environ.get('REDIS_URL') or 'redis://'


class Settings():
    """Settings object"""
    settings_funcs = {}

    @classmethod
    def register(cls, obj_name):
        """Register a settings function

        A settings function returns a settings dict associated with an 
        object name. The settings dict maps object attribute names to 
        values. These attributes are set when an object is initialized.
        """
        def wrapper(func):
            if obj_name not in cls.settings_funcs:
                cls.settings_funcs[obj_name] = []
            cls.settings_funcs[obj_name].append(func)
            return func()
        return wrapper

    @classmethod
    def get(cls, *obj_names):
        """Get the settings associated with a list of object names

        Settings functions associated with the same object name override 
        settings functions registered previously.
        """
        settings = {}
        for obj_name in obj_names:
            funcs = cls.settings_funcs.get(obj_name)
            if funcs:
                [settings.update(func()) for func in funcs]
        return settings


TIME_EXPIRED_TXT = 'You have exceeded your time limit for this survey'

RESTART_TXT = """
<p>Click << to return to your in progress survey. Click >> to restart the survey.</p>
<p>If you choose to restart the survey, your responses will not be saved.</p>
"""

SCREENOUT_TXT = """
<p>Our records indicate that you have already participated in this or similar surveys.</p>
<p>Thank you for your continuing interest in our research.</p>
"""

SOCKET_JS_SRC = 'https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js'

@Settings.register('app')
def settings():
    return {
        'clean_data': None,
        'duplicate_keys': [],
        'offline': False,
        'password': '',
        'restart_option': True,
        'restart_text': RESTART_TXT,
        'screenout_folder': None,
        'screenout_keys': ['IPv4', 'workerId'],
        'screenout_text': SCREENOUT_TXT,
        'socket_js_src': SOCKET_JS_SRC,
        'static_folder': 'static',
        'status_log_period': '00:02:00',
        'template_folder': 'templates',
        'time_expired_text': TIME_EXPIRED_TXT,
        'time_limit': None,
    }

@Settings.register('manager')
def settings():
    return {
        'loading_img_blueprint': 'hemlock',
        'loading_img_filename': 'img/worker_loading.gif'
    }

def get_app_settings():
    """Get application settings
    
    Convert settings to timedelta objects as needed.
    
    Then merge static and template folders with current working directory. 
    Return these separately, as they need to be passed to the Flask 
    constructor.
    """
    settings = Settings.get('app')
    to_timedelta(settings, 'time_limit')
    to_timedelta(settings, 'status_log_period')

    password = settings.pop('password', '')
    settings['password_hash'] = generate_password_hash(password)
    static = os.path.join(os.getcwd(), settings.pop('static_folder'))
    templates = os.path.join(os.getcwd(), settings.pop('template_folder'))
    return settings, static, templates

def to_timedelta(settings, key):
    """Convert time expressed as 'hh:mm:ss' to timedelta object"""
    time_str = settings[key]
    if time_str is None:
        return
    t = datetime.strptime(time_str, '%H:%M:%S')
    settings[key] = timedelta(hours=t.hour,minutes=t.minute,seconds=t.second)

def get_screenouts(app):
    """Store screenouts dictionary as application attribute"""
    if not app.screenout_folder:
        app.screenouts = None
        return
    app.screenout_folder = os.path.join(os.getcwd(), app.screenout_folder)
    screenout_csvs = glob(app.screenout_folder+'/*.csv')
    df = pd.concat([pd.read_csv(csv) for csv in screenout_csvs]).astype(str)
    app.screenouts = df.to_dict(orient='list')