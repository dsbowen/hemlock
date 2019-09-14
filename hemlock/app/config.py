"""Configuration object"""

import os

class Config():
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = (
        os.environ.get('DATABASE_URL') 
        or 'sqlite:///'+os.path.join(os.getcwd(), 'data.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WKHTMLTOIMAGE = os.environ.get('WKHTMLTOIMAGE')
    