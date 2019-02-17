###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 02/17/2019
###############################################################################

'''
TODO:
record empty dataframe
back for branch embedded dataframe
relationships instead of queries
routes folder and submodules
general cleaning
vaidation bank
'''

from hemlock import create_app, db, query, restore_branch, even_randomize, random_assignment, Participant, Branch, Page, Question, Choice, Validator, Variable, Randomizer
from hemlock.validation_bank import *
from config import Config
import pandas as pd
import numpy as np
from random import choice

def Start():
    b = Branch()
    
    p = Page(b)
    Question(p, '''
        Survey instructions
    '''
    
    
    
    return b
        
app = create_app(Config, 
    start=Start, 
    password='123',
    record_incomplete=True,
    block_duplicate_ips=False,
    block_from_csv='block.csv')

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'query':query, 'restore_branch':restore_branch, 'even_randomize':even_randomize, 'random_assignment':random_assignment,'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable, 'pd':pd, 'np':np, 'Randomizer':Randomizer}