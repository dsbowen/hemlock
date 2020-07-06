"""## Default application settings

Below are the default settings for Hemlock applications and extensions.

App settings
------------
clean_data : callable or None, default=None
    Callable which cleans your data before downloading or creating a data 
    profile. This callable takes and returns `pandas.DataFrame`. If `None`, no
    additional cleaning is performend.

duplicate_keys : list, default=[]
    List of keys (column names) on which to block duplicate participants. If
    empty, the app will not screen out duplicates.

password : str, default=''
    Password for accessing the researcher dashboard.

restart_option : bool, default=True
    Indicates that participants who attempt to re-navigate to the index page 
    will be given the option to restart the survey. If `False`, participants 
    to attempt to re-navigate to the index page will be redirected to their 
    current survey page.

restart_text : str, default='Click << to return...'
    Text displayed to participants when given the option to restart or 
    continue with the survey.

screenout_csv : str, default='screenout.csv'
    Name of the csv file containing criteria for screening out participants.

screenout_keys : list, default=[]
    List of keys (column names) on which to screen out participants. If empty,
    participants will be screened out based on all keys in the screenout csv.

screenout_text : str, default='...you have already participated...'
    Text displayed to participants who are ineligible to participate in this 
    survey.

socket_js_src : str, default='https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.3.0/socket.io.js'
    Source of the websocket javascript.

static_folder : str, default='static'
    Path to the static folder.

template_folder : str, default='templates'
    Path to the template folder.

time_expired_text : str, default='You have exceeded your time limit...'
    Text displayed to participants whose time has expired.

time_limit : datetime.timedelta or None, default=None
    Time limit for participants to complete the survey.

validate : bool, default=True
    Indicate that all validation is active. Set to `False` to turn off all 
    validation for testing.

Config
------
SECRET_KEY : str
    Looks for a `SECRET_KEY` environment variable.

SQLALCHEMY_DATABASE_URI : str
    Looks for `DATABASE_URL` environment variable. Otherwise, we use a SQLite 
    database `data.db` in the current working directory.

SQLALCHEMY_TRACK_MODIFICATIONS: bool, default=False

REDIS_URL : str, default='redis://'
    Looks for a `REDIS_URL` environment variable.

DownloadBtnManager
------------------

Manager
-------
loading_img_blueprint : str or None, default='hemlock'
    Name of the blueprint to which the loading image belongs. If `None`, the 
    loading image is assumed to be in the app's `static` directory.

loading_img_filename : str or None, default='img/worker_loading.gif'
    Name of the loading image file.

Notes
-----
See <https://flask.palletsprojects.com/en/1.1.x/config/> for more detail on 
Flask application configuration.

See <https://dsbowen.github.io/flask-download-btn/manager/> for more detail on 
DownloadBtnManager settings.

See <https://dsbowen.github.io/flask-worker/manager/> for more detail on 
Manager settings.
"""

import os

RESTART_TXT = """
<p>Click << to return to your in progress survey. Click >> to restart the survey.</p>
<p>If you choose to restart the survey, your responses will not be saved.</p>
"""

SCREENOUT_TXT = """
<p>Our records indicate that you have already participated in this or similar surveys.</p>
<p>Thank you for your continuing interest in our research.</p>
"""

SOCKET_JS_SRC = 'https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.3.0/socket.io.js'

TIME_EXPIRED_TXT = 'You have exceeded your time limit for this survey'

settings = {
    'clean_data': None,
    'duplicate_keys': [],
    'password': '',
    'restart_option': True,
    'restart_text': RESTART_TXT,
    'screenout_csv': 'screenout.csv',
    'screenout_keys': [],
    'screenout_text': SCREENOUT_TXT,
    'socket_js_src': SOCKET_JS_SRC,
    'static_folder': 'static',
    'template_folder': 'templates',
    'time_expired_text': TIME_EXPIRED_TXT,
    'time_limit': None,
    'validate': True,
    'Config': {
        'SECRET_KEY': os.environ.get('SECRET_KEY') or 'secret-key',
        'SQLALCHEMY_DATABASE_URI': (
            os.environ.get('DATABASE_URL')
            or 'sqlite:///'+os.path.join(os.getcwd(), 'data.db')
        ),
        'SQLALCHEMY_TRACK_MODIFICATIONS': False,
        'REDIS_URL': os.environ.get('REDIS_URL') or 'redis://',
    },
    'DownloadBtnManager': {},
    'Manager': {
        'loading_img_blueprint': 'hemlock',
        'loading_img_filename': 'img/worker_loading.gif'
    },
}