###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 02/10/2019
###############################################################################

from hemlock import create_app, db, query, Participant, Branch, Page, Question, Choice, Validator, Variable
from config import Config
import pandas as pd

def Start():
    b = Branch()
    
    x = pd.read_csv('mycsv.csv')
    hello = x['hello']
    p = Page(branch=b)
    for celestial_body in hello:
        q = Question(page=p, text='Hello, {0}'.format(celestial_body))
    
    p = Page(branch=b)
    q = Question(page=p, text='hello world')
    
    q = Question(page=p, qtype='single choice', var='yes', text='Please say yes', randomize=True)
    c = Choice(question=q, text='yes')
    c = Choice(question=q, text='no')
    v = Validator(question=q, condition=yes)
    
    p = Page(branch=b)
    q = Question(page=p, qtype='free', var='yes', text='Please say no')
    v = Validator(question=q, condition=no)
    
    p = Page(branch=b, randomize=True)
    q = Question(page=p, qtype='single choice', var='yes', text='Answer what you wish', randomize=True, post=post)
    c = Choice(question=q, text='yes')
    c = Choice(question=q, text='no')
    v = Validator(question=q, condition=force)
    p.set_next(Next, q.id)
    
    b.set_next(End, q.id)
    
    return b
    
def yes(q):
    entry = q.get_entry()
    if entry is None or entry.lower() != 'yes':
        return "Please say yes"
        
def no(q):
    entry = q.get_entry()
    if entry is None or entry.lower() != 'no':
        return "Please say no"
        
def force(q):
    if q.get_entry() is None:
        return "Please answer the question"
        
def Next(wish_id):
    b = Branch()
    YES = query(wish_id).get_entry().upper()
    q = Question(branch=b, var='YES', data=YES)
    return b
        
def End(wish_id):
    b = Branch()
    p = Page(branch=b, terminal=True, render=wish, render_args=wish_id)
    q = Question(page=p, render=not_wish, render_args=wish_id)
    return b
    
def wish(page, wish_id):
    wish = query(wish_id).get_entry()
    q = Question(page=page, text='You wished to answer {0}'.format(wish))
    
def not_wish(q, wish_id):
    not_wish = query(wish_id).get_nonselected()[0].get_text()
    q.set_text('You did not wish to answer {0}'.format(not_wish))
    
def post(q):
    q.set_data(q.get_entry()=='yes')
        
app = create_app(Config, 
    start=Start, 
    block_duplicate_ips=True)#,
    #block_from_csv='block.csv')

@app.shell_context_processor
def make_shell_context():
    return {'db':db, 'query':query, 'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable}