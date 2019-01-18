from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from hemlock.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

from hemlock import routes