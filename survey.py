###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 02/27/2019
###############################################################################

'''
TODO:
general cleaning, incl routes folder and relationships (as opposed to queries)
for debugging, pass args to start function
back for branch embedded dataframe
record empty dataframe
vaidation bank
css - larger margins
page needs all_rows
also timer function
next branch id stuff not working
'''

from hemlock import create_app, db, query, restore_branch, even_randomize, random_assignment, modg, g, comprehension_check, Participant, Branch, Page, Question, Choice, Validator, Variable, Randomizer
from hemlock.validation_bank import *
from config import Config
import pandas as pd
import numpy as np
from random import choice, shuffle
from copy import deepcopy
from flask_login import current_user

from texts import *

def Start():
    raise NotImplementedError()
        
app = create_app(Config, 
    start=Start, 
    password='',
    record_incomplete=False,
    block_duplicate_ips=False,
    block_from_csv='block.csv')

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'query':query, 'restore_branch':restore_branch, 'even_randomize':even_randomize, 'random_assignment':random_assignment,'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable, 'pd':pd, 'np':np, 'Randomizer':Randomizer}