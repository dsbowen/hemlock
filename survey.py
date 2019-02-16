###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 02/15/2019
###############################################################################

'''
TODO
CHECKPOINTS TO FIX THIS BUG
'''

from hemlock import create_app, db, query, restore_branch, Participant, Branch, Page, Question, Choice, Validator, Variable
from config import Config
import pandas as pd
import numpy as np
from random import choice

#https://getbootstrap.com/docs/4.0/components/forms/

'''
Cases:
    crossing:
        pages within a branch
        branch with next function
        branch without next function
        page branch with next function
        page branch without next function
    restore:
        0, 1 and 2 on back
        0, 1 and 2 on invalid
        0, 1, 2 on forward
        with and without post and render functions
'''

def Start():
    b = Branch(next=Next)
    b.next(args=b.id)
    
    p = Page(b)
    Question(p, 'hello world')
    
    return b
    
def Next1():
    return Branch()
    
def Next2():
    return Branch(next=Next3)
    
def Next3():
    b = Branch()
    p = Page(b, back=True, next=Next4)
    p.next(args=p.id)
    Question(p, 'next 3')
    return b
    
def Next4(prev_id):
    branch = restore_branch(prev_id, Page)
    if branch is not None:
        return branch
    b = Branch()
    p = Page(b, back=True)
    Question(p, 'free response', 'free', 'free', all_rows=True)
    return b
    
def Next(prev_id):
    branch = restore_branch(prev_id)
    if branch is not None:
        return branch

    b=Branch()
    
    p = Page(b, back=True)
    q = Question(p, 'yes or no?', 'free', 'yes_no', default='yes', all_rows=True)
    Validator(q, require)
    p.next(Next1)
    
    p = Page(b, back=True)
    p.restore_on({'invalid':1})
    q = Question(p, 'high or low?', 'free', 'high_low', default='high', all_rows=True)
    Validator(q, require)
    p.next(Next2)
    
    p = Page(b, restore_on={'back':1})
    p.back()
    q = Question(p, 'pick one', 'single choice', 'one')
    Choice(q, 'one', 1)
    q.randomize()
    q.default(Choice(q, 'two', 0))
    Choice(q, 'three', 0)
    Validator(q, one)
    q.post(add, ['four',0])
    
    p = Page(b, restore_on={'forward':1}, back=True)
    q = Question(p, 'pick one', 'single choice', 'one', randomize=True)
    q.default(Choice(q, 'one', 0))
    Choice(q, 'two', 1)
    Choice(q, 'three', 0)
    Validator(q, one, 'Just kidding, pick two')
    q.post(add, ['seven',0])
    
    p = Page(b, restore_on={'forward':0,'invalid':0}, back=True)
    q = Question(p, 'pick three (no tricks this time!)', 'single choice', 'one', randomize=True)
    q.default(Choice(q, 'one', 0))
    Choice(q, 'two', 0)
    Choice(q, 'three', 1)
    Validator(q, one, "That's not what I said...")
    q.render(add2, p.id)
    
    p = Page(b, back=True, terminal=True)
    Question(p, 'hello moon')
    
    return b
    
def add2(q, p_id):
    p = query(p_id, Page)
    if query(p_id, Page).get_direction()=='invalid':
        q.default(Choice(q, choice(['buttercups', 'cherry blossoms']), 1))
        q.text(q.get_text()+' Buttercups and cherry blossoms will also do :)')

def add(q, args):
    num, val = args
    order = choice([0,1,2,3])
    q.default(Choice(q, num, val, order=order))
    
def require(q):
    response = q.get_response()
    if response is None or response == '':
        return 'Please answer the question'
        
def one(q, message=None):
    if not q.get_data():
        if message is None:
            return 'I said pick one!'
        return message

# def Start():
    # b = Branch(next=End)
    
    # p = Page(b, next=Middle)
    # q = Question(p, 'Hello world')
    
    # p = Page(b, randomize=True, restore_on={'invalid':2}, back=True)
    # q = Question(p, 'Hello moon', 'free', 'hello', default='hello moon', post=post)
    # Validator(q, required)
    # q = Question(p, 'Hello star', 'free', 'hello', default='hello star')
    # Validator(q, required)
    
    # return b
    
# def Middle():
    # b = Branch()
    # p = Page(b)
    # Question(p, 'Middle')
    # return b
    
# def post(q):
    # q.text('Goodbye moon')
    
# def End():
    # b = Branch()

    # p = Page(b, randomize=True, restore_on={'invalid':1})
    # q = Question(p, 'Goodbye', 'single choice', 'goodbye', True, all_rows=True)
    # Choice(q, 'Goodbye world')
    # Choice(q, 'Goodbye moon')
    # Choice(q, 'Goodbye star')
    # Validator(q, required)
    
    # q = Question(p, 'Comprehension check', 'single choice', 'comp', all_rows=True)
    # q.default(Choice(q, 'correct', 1))
    # Choice(q, 'incorrect', 0)
    # Choice(q, 'also incorrect', 0)
    # Validator(q, required)
    # Validator(q, attn)
    
    # p = Page(b, terminal=True)
    # Question(p, 'Thank you for participating!')
    
    # return b
    

        
# def attn(q):
    # if not q.get_data():
        # return 'Your response was incorrect'


# def Start():
    # v = Validator()
    # u = Validator()
    # u.condition(foo)
    # v._copy(u.id)
    # db.session.commit()
    # print(u._condition_function)
    # print(v._condition_function)
    # u.condition(bar)
    # print(u._condition_function)
    # print(v._condition_function)
    
    # c = Choice()
    # d = Choice()
    # c.text('hello moon')
    # print(d._text)
    # d._copy(c.id)
    # print(d._text)
    # c.text('hello star')
    # print(c._text)
    # print(d._text)
    
    # x = Question.__table__.columns
    # [print(i) for i in x]
    # x = Question.__table__.foreign_keys
    # print('foreign keys')
    # [print(i) for i in x]
    
    # q = Question()
    # p = Question()
    # q._copy(p.id)
    # q.render(foo)
    # db.session.commit()
    # p._copy(q.id)
    # x = q.__table
    
    # b = Branch()
    # p = Page(branch=b, terminal=True)
    # q = Question(page=p, text='hello world')
    # return b

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
    # response = q.get_response()
    # if response is None or response.lower() != 'yes':
        # return "Please say yes"
        
# def no(q):
    # response = q.get_response()
    # if response is None or response.lower() != 'no':
        # return "Please say no"
        
# def force(q):
    # if q.get_response() is None:
        # return "Please answer the question"
        
# def render(page, branch_id):
    # b = query(branch_id, Branch)
    # q = Question(branch=b, var='test', data=1, all_rows=True)
        
# def Next(wish_id):
    # b = Branch()
    # YES = query(wish_id).get_response().upper()
    # q = Question(branch=b, var='YES', data=YES)
    # return b
        
# def End(wish_id):
    # b = Branch()
    # p = Page(branch=b, terminal=True, render=wish, render_args=wish_id)
    # q = Question(page=p, render=not_wish, render_args=wish_id)
    # return b
    
# def wish(page, wish_id):
    # wish = query(wish_id).get_response()
    # q = Question(page=page, text='You wished to answer {0}'.format(wish))
    
# def not_wish(q, wish_id):
    # not_wish = query(wish_id).get_nonselected()[0].get_text()
    # q.text('You did not wish to answer {0}'.format(not_wish))
    
# def post(q):
    # q.data(q.get_response()=='yes')
        
app = create_app(Config, 
    start=Start, 
    block_duplicate_ips=False,
    block_from_csv='block.csv')

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'query':query, 'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable, 'pd':pd, 'np':np}