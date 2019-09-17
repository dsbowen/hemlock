"""Application default settings and configuration object

time_limit must be input in 'hh:mm:ss' format.
"""

import os

BACK_BUTTON = """
    <button id="back-button" name="direction" type="submit" class="btn btn-outline-primary" style="float: left;" value="back"> 
    << 
    </button>
"""

FORWARD_BUTTON = """
    <button id="forward-button" name="direction" type="submit" class="btn btn-outline-primary" style="float: right;" value="forward">
    >> 
    </button>
"""

def page_compile(page):
    """Calls question compile functions in index order"""
    return [q.compile(object=q) for q in page.questions]
    
def page_post(page):
    """Calls question post functions in index order"""
    return [q.post(object=q) for q in page.questions]

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
    'question_post': None,
    'restart_option': True,
    'screenout_folder': 'screenouts',
    'screenout_keys': ['IPv4', 'workerId'],
    'static_folder': 'static',
    'survey_template': 'default_survey.html',
    'template_folder': 'templates',
    'time_limit': None,
    'view_template': 'default_view.html'
    }

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') 
        or 'sqlite:///'+os.path.join(os.getcwd(), 'data.db')
        )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WKHTMLTOIMAGE = os.environ.get('WKHTMLTOIMAGE')
    