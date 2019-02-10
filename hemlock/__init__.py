from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy

bp = Blueprint('hemlock', __name__)
db = SQLAlchemy()

def create_app(config_class, start):
	app = Flask(__name__)
	app.config.from_object(config_class)
	app.start = start
	
	db.init_app(app)
	
	app.register_blueprint(bp)
	
	return app

from hemlock import routes
from hemlock.query import query
from hemlock.models.participant import Participant
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question
from hemlock.models.choice import Choice
from hemlock.models.validator import Validator
from hemlock.models.variable import Variable