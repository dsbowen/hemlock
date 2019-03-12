###############################################################################
# Hemlock shell context processor
# by Dillon Bowen
# last modified 03/11/2019
###############################################################################

from survey import *
import pandas as pd
import numpy as np
from random import choice, shuffle
from copy import deepcopy
from flask_login import current_user
from hemlock.models.variable import Variable
from hemlock.randomize_tools import Randomizer
from hemlock.factory import db
# from hemlock import create_app, db, query, restore_branch, even_randomize, random_assignment, modg, g, comprehension_check, Participant, Branch, Page, Question, Choice, Validator, Variable, Randomizer

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'query':query, 'restore_branch':restore_branch, 'even_randomize':even_randomize, 'random_assignment':random_assignment,'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable, 'pd':pd, 'np':np, 'Randomizer':Randomizer}