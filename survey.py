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
    b = Branch(next=Next)
        
    p1 = Page(b, timer='myvar_time')
    Question(p1, 'free response 1', 'free', 'myvar')
    
    p2 = Page(b, back=True, timer='myvar_time')
    q =Question(p2, 'free response 2', 'free', 'myvar')
    Validator(q, require)
    
    p = Page(b, back=True)
    Question(p, 'Empty page')
    Question(p, qtype='embedded', var='embedded', data='this is not the end', all_rows=True)
    
    return b
        
def Next():
    b = Branch()
    p = Page(b, timer='myvar2_time', back=True)
    q = Question(p, 'mc', 'single choice', 'myvar2')
    q.default(Choice(q, 'choice 1'))
    Choice(q, 'choice 2')
    p.next(Next2)
    
    p = Page(b, back=True, terminal=True)
    Question(p, 'Thank you')
    
    return b
    
def Next2():
    b = Branch(next=Next3)
    p = Page(b, back=True)
    Question(p, 'next2')
    return b
    
def Next3():
    b = Branch()
    return b
        
def require(q):
    if q.get_response() is None or q.get_response() == '':
        return 'Please respond'
    
        
app = create_app(Config, 
    start=Start, 
    record_incomplete=True,
    block_duplicate_ips=False,
    block_from_csv='block.csv')

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'query':query, 'restore_branch':restore_branch, 'even_randomize':even_randomize, 'random_assignment':random_assignment,'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable, 'pd':pd, 'np':np, 'Randomizer':Randomizer}