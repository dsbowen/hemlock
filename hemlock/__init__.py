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