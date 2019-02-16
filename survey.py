###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 02/15/2019
###############################################################################

'''
RECORD EMPY DATAFRAME
'''

from hemlock import create_app, db, query, restore_branch, even_randomize, random_assignment, Participant, Branch, Page, Question, Choice, Validator, Variable, Randomizer
from config import Config
import pandas as pd
import numpy as np
from random import choice

#https://getbootstrap.com/docs/4.0/components/forms/

def Start():
    b = Branch()
    
    disclosed = [0,1]
    smart_anchor = [0,1]
    # disclosed, smart_anchor = random_assignment(b,'condition',
        # ['disclosed', 'smart_anchor'], [disclosed, smart_anchor])
        
    p1 = Page(b, back=True)
    Question(p1, 'free response 1', 'free', 'myvar')
    
    p2 = Page(b)
    q =Question(p2, 'free response 2', 'free', 'myvar')
    Validator(q, world)
    Validator(q, require, order=0)
    
    p1.branch(b)
    
    p = Page(b, terminal=True, back=True)
    Question(p, 'Empty page')
    Question(p, qtype='embedded', var='myvar2', data='this is the end', all_rows=True)
    
    return b
    
def world(q):
    if q.get_response() != 'world':
        return 'world'
        
def require(q):
    if q.get_response() is None or q.get_response() == '':
        return 'Please respond'
    
def disp(q, assignments):
    disclosed, smart_anchor = assignments
    if disclosed:
        knowledge = 'disclosed'
    else:
        knowledge = 'surprise'
    if smart_anchor:
        anchor = 'smart anchor'
    else:
        anchor = 'no anchor'
    q.text('You are in the {0} {1} condition'.format(knowledge, anchor))
        
app = create_app(Config, 
    start=Start, 
    record_incomplete=True,
    block_duplicate_ips=False,
    block_from_csv='block.csv')

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'query':query, 'restore_branch':restore_branch, 'even_randomize':even_randomize, 'random_assignment':random_assignment,'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable, 'pd':pd, 'np':np, 'Randomizer':Randomizer}