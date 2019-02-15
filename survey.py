###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 02/14/2019
###############################################################################

from hemlock import create_app, db, query, Participant, Branch, Page, Question, Choice, Validator, Variable
from config import Config
import pandas as pd
import numpy as np

#https://getbootstrap.com/docs/4.0/components/forms/
'''
NOTE: need to store errors if restoring to s1 on invalid
TO SPEED UP: HAVE ANOTHER OBJECT AS INPUT FOR __INIT__ AND COPY
make sure order is being recorded correctly before moving on
TODO
store errors in s1
test restore s1 on invalid
add back button
store state s2 on back
restore previous page
in participant have a single page queue - no branch stack per se
need something like next functions in the queue
keep track of when next function should be called in participant
participant head moves along queue
first make it work for a single branch
or maybe don't need to do this for monday

'''

def Start():
    b = Branch(next=End)
    
    p = Page(b)
    Question(p, 'Hello world')
    
    p = Page(b, randomize=True)
    q = Question(p, 'Hello moon', 'free', 'hello')
    q.default('hello moon')
    q = Question(p, 'Hello star', 'free', 'hello')
    q.default('hello star')
    
    p = Page(b)
    q = Question(p, 'Pick one', 'single choice', 'hello', True)
    Choice(q, 'hello world')
    Choice(q, 'hello moon')
    c = Choice(q, 'hello star')
    q.default(c.id)
    
    return b
    
def End():
    b = Branch()

    p = Page(b, randomize=True)
    q = Question(p, 'Goodbye', 'single choice', 'goodbye', True, all_rows=True)
    Choice(q, 'Goodbye world')
    Choice(q, 'Goodbye moon')
    c = Choice(q, 'Goodbye star')
    q.default(c.id)
    Validator(q, required)
    
    q = Question(p, 'Comprehension check', 'single choice', 'comp', all_rows=True)
    c = Choice(q, 'correct', 1)
    q.default(c.id)
    Choice(q, 'incorrect', 0)
    Choice(q, 'also incorrect', 0)
    Validator(q, required)
    Validator(q, attn)
    
    p = Page(b, terminal=True)
    Question(p, 'Thank you for participating!')
    
    return b
    
def required(q):
    if q.get_response() is None:
        return 'Please answer the question'
        
def attn(q):
    if not q.get_data():
        return 'Your response was incorrect'

# def foo():
    # return 10
    
# def bar():
    # return 11

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