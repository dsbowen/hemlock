###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 02/15/2019
###############################################################################

'''
syntax: x = even_randomize(tag, nested list or tuples, choose_num, combination)
MIGHT HAVE TO DO DEEP COPIES TO CHANGE ARGS
'''

from hemlock import create_app, db, query, restore_branch, even_randomize, random_assignment, Participant, Branch, Page, Question, Choice, Validator, Variable
from config import Config
import pandas as pd
import numpy as np
from random import choice

#https://getbootstrap.com/docs/4.0/components/forms/



def Start():
    b = Branch()
    
    disclosed = [0,1]
    smart_anchor = [0,1]
    knowledge, anchor = random_assignment('condition',[disclosed,smart_anchor])
    disclosed = Question(branch=b, qtype='embedded', var='disclosed', data=knowledge, all_rows=True)
    smart_anchor = Question(branch=b, qtype='embedded', var='smart_anchor', data=anchor, all_rows=True)
    
    p = Page(b, terminal=True)
    q = Question(p, render=disp_condition, render_args=[disclosed.id,smart_anchor.id])
    
    return b
    
def disp_condition(q, condition_ids):
    disclosed, smart_anchor = query(condition_ids)
    if disclosed.get_data():
        knowledge = 'disclosed'
    else:
        knowledge = 'surprise'
    if smart_anchor.get_data():
        anchor = 'smart anchor'
    else:
        anchor = 'no anchor'
    q.text('You are in the {0} {1} condition'.format(knowledge, anchor))
        
app = create_app(Config, 
    start=Start, 
    block_duplicate_ips=False,
    block_from_csv='block.csv')

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'query':query, 'restore_branch':restore_branch, 'even_randomize':even_randomize, 'random_assignment':random_assignment,'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable, 'pd':pd, 'np':np, 'Randomizer':Randomizer}