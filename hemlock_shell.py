"""Hemlock shell context processor"""

from hemlock import *
from hemlock.app import db
import pandas as pd
import numpy as np
import random

from app import app

@app.shell_context_processor
def make_shell_context():
    db.create_all()
    return globals()