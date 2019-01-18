from flask import Flask
from hemlock.config import Config

app = Flask(__name__)
app.config.from_object(Config)

from hemlock import routes