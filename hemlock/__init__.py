from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash
import pandas as pd

bp = Blueprint('hemlock', __name__)
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'hemlock.index'
bootstrap = Bootstrap()

def create_app(config_class, start, password='', record_incomplete=False,
    block_duplicate_ips=True, block_from_csv=None):
    
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    app.start = start
    app.password_hash = generate_password_hash(password)
    app.record_incomplete = record_incomplete
    app.block_dupips = block_duplicate_ips
    app.ipv4_csv, app.ipv4_current = [], []
    if block_from_csv is not None:
        app.ipv4_csv = list(pd.read_csv(block_from_csv)['ipv4'])
    
    db.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)
    
    app.register_blueprint(bp)
    
    return app

from hemlock import routes
from hemlock.query import query
from hemlock.restore_branch import restore_branch
from hemlock.randomize_tools import even_randomize, random_assignment, Randomizer
from hemlock.models.participant import Participant
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.choice import Choice
from hemlock.models.validator import Validator
from hemlock.models.variable import Variable