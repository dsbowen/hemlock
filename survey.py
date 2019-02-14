###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 02/10/2019
###############################################################################

from hemlock import create_app, db, query, Participant, Branch, Page, Question, Choice, Validator, Variable
from config import Config
import pandas as pd
import numpy as np

#https://getbootstrap.com/docs/4.0/components/forms/

# _copy(object id)
# get object by query
# get column keys: inspect(Table).columns.keys()
# copy all column keys except id
# get relationship keys: inspect(Table).relationships.keys()
# filter out parents and keep children:
#  x = list(inspect(Table).relationships)
#  keep relationship key i if x[i].direction.name == 'ONETOMANY'
# create list of children and assign to self
# _copy children
# store copy id in self

# _restore to s2:
# store errors in ordered list
# _copy(s2.id)
# assign errors

# _restore to s1:
# create a copy
# _copy(s1.id)
# store s3 copy
# can conditionally reference s3 during rendering


def foo():
    return 10
    
def bar():
    return 11

def Start():
    v = Validator()
    u = Validator()
    u.condition(foo)
    v._copy(u.id)
    db.session.commit()
    print(u._condition_function)
    print(v._condition_function)
    u.condition(bar)
    print(u._condition_function)
    print(v._condition_function)
    
    c = Choice()
    d = Choice()
    c.text('hello moon')
    print(d._text)
    d._copy(c.id)
    print(d._text)
    c.text('hello star')
    print(c._text)
    print(d._text)
    
    x = Question.__table__.columns
    [print(i) for i in x]
    x = Question.__table__.foreign_keys
    print('foreign keys')
    [print(i) for i in x]
    
    q = Question()
    p = Question()
    q._copy(p.id)
    q.render(foo)
    db.session.commit()
    p._copy(q.id)
    x = q.__table
    # print(p._render_function)
    
    b = Branch()
    p = Page(branch=b, terminal=True)
    q = Question(page=p, text='hello world')
    return b

# def Start():
    # b = Branch(randomize=True)
    
    # p = Page(branch=b, randomize=True)
    # q = Question(page=p, text='hello world')
    
    # q = Question(page=p, qtype='single choice', var='yes', text='Please say yes', randomize=True, clear_on=['invalid'])
    # c = Choice(question=q, text='yes')
    # c = Choice(question=q, text='no', value=0)
    # c = Choice(question=q, text='maybe', value=0)
    # q.default(c.id)
    # v = Validator(question=q, condition=yes)
    
    # p = Page(branch=b, render=render, render_args=b.id)
    # q = Question(page=p, qtype='free', var='yes', text='Please say no', default='no', clear_on=['invalid'])
    # v = Validator(question=q, condition=no)
    
    # p = Page(branch=b, randomize=True)
    # q = Question(page=p, qtype='single choice', var='yes', text='Answer what you wish', randomize=True, post=post, clear_on=['invalid'])
    # c = Choice(question=q, text='yes')
    # c = Choice(question=q, text='no')
    # v = Validator(question=q, condition=force)
    # p.next(Next, q.id)
    
    # b.next(End, q.id)
    
    # return b
    
# def yes(q):
    # entry = q.get_entry()
    # if entry is None or entry.lower() != 'yes':
        # return "Please say yes"
        
# def no(q):
    # entry = q.get_entry()
    # if entry is None or entry.lower() != 'no':
        # return "Please say no"
        
# def force(q):
    # if q.get_entry() is None:
        # return "Please answer the question"
        
# def render(page, branch_id):
    # b = query(branch_id, Branch)
    # q = Question(branch=b, var='test', data=1, all_rows=True)
        
# def Next(wish_id):
    # b = Branch()
    # YES = query(wish_id).get_entry().upper()
    # q = Question(branch=b, var='YES', data=YES)
    # return b
        
# def End(wish_id):
    # b = Branch()
    # p = Page(branch=b, terminal=True, render=wish, render_args=wish_id)
    # q = Question(page=p, render=not_wish, render_args=wish_id)
    # return b
    
# def wish(page, wish_id):
    # wish = query(wish_id).get_entry()
    # q = Question(page=page, text='You wished to answer {0}'.format(wish))
    
# def not_wish(q, wish_id):
    # not_wish = query(wish_id).get_nonselected()[0].get_text()
    # q.text('You did not wish to answer {0}'.format(not_wish))
    
# def post(q):
    # q.data(q.get_entry()=='yes')
        
app = create_app(Config, 
    start=Start, 
    block_duplicate_ips=False,
    block_from_csv='block.csv')

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'query':query, 'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable, 'pd':pd, 'np':np}