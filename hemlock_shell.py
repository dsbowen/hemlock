###############################################################################
# Hemlock shell context processor
# by Dillon Bowen
# last modified 03/12/2019
###############################################################################

from survey import app
from hemlock import *
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
    
    # hemlock tools
    'comprehension_check':comprehension_check,
    'modg':modg,
    'g':g,
    'query':query,
    'even_randomize':even_randomize, 
    'random_assignment':random_assignment,
    'restore_branch':restore_branch,
    'requre':require,
    'integer':integer,
    'in_range':in_range,
    
    # additional tools
    'pd':pd, 
    'np':np,
    'random':random}