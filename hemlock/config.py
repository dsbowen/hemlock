###############################################################################
# Configuration file for Hemlock survey append
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

import os
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uA%G?{wVEH&`@As'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///'+os.path.join(basedir, 'data.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False