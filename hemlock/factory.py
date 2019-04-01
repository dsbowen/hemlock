###############################################################################
# Application factory
# by Dillon Bowen
# last modified 03/11/2019
###############################################################################

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap
from werkzeug.security import generate_password_hash
import pandas as pd

# create blueprint, database, login, and bootstrap
bp = Blueprint('hemlock', __name__)
db = SQLAlchemy()
login = LoginManager()
login.login_view = 'hemlock.login'
bootstrap = Bootstrap()

'''
Application factory

Arguments:
    config_class: configures application by object
    start: starting navigation function in survey
    password: password for accessing researcher urls
    record_incomplete: indicates incomplete responses should be recorded
    block_duplicates: indicates duplicate IP addresses should be blocked
    block_from_csv: csv file containing IP addresses to block
'''
def create_app(
        config_class, 
        start, 
        password='', 
        record_incomplete=False,
        block_duplicate_ips=True, 
        block_from_csv=None):
    
    # configure application
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # set application parameters
    app.start = start
    app.password_hash = generate_password_hash(password)
    app.record_incomplete = record_incomplete
    app.block_dupips = block_duplicate_ips
    app.ipv4_csv, app.ipv4_current = [], []
    if block_from_csv is not None:
        app.ipv4_csv = list(pd.read_csv(block_from_csv)['ipv4'])
    
    # initialize application features
    db.init_app(app)
    login.init_app(app)
    bootstrap.init_app(app)
    
    # register the application blueprint
    app.register_blueprint(bp)
    
    return app