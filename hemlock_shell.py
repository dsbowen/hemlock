##############################################################################
# Hemlock shell context processor
# by Dillon Bowen
# last modified 09/06/2019
##############################################################################

from survey import app
from hemlock import *
from hemlock.factory import db
import pandas as pd
import numpy as np
import random

@app.shell_context_processor
def make_shell_context():
    db.create_all()
    return globals()