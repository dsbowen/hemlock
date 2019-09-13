"""Hemlock shell context processor"""

from survey import *
from hemlock.factory import db
import pandas as pd
import numpy as np
import random

@app.shell_context_processor
def make_shell_context():
    db.create_all()
    return globals()