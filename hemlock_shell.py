###############################################################################
# Hemlock shell context processor
# by Dillon Bowen
# last modified 03/17/2019
###############################################################################

from survey import app
from hemlock import *
from hemlock.models.private import *
from hemlock.factory import db
import pandas as pd
import numpy as np
import random

@app.shell_context_processor
def make_shell_context():
    return {    
    # models
    'Participant':Participant, 
    'Branch':Branch, 
    'Page':Page, 
    'Question':Question, 
    'Choice':Choice, 
    'Validator':Validator,
    'Visitors': Visitors,
    
    # hemlock tools
    'comprehension_check':comprehension_check,
    'modg':modg,
    'g':g,
    'query':query,
    'even_randomize':even_randomize, 
    'random_assignment':random_assignment,
    'requre':require,
    'integer':integer,
    'in_range':in_range,
    
    # additional tools
    'pd':pd, 
    'np':np,
    'random':random,

    # database
    'db':db,
    
    # private models
    'Visitors':Visitors}