###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock import create_app, db, query, Participant, Branch, Page, Question, Choice, Validator, Variable
from config import Config

def Start():
    b = Branch(next=End, randomize=True)
    
    p = Page(branch=b)
    q = Question(page=p, qtype='single choice', text='Please say yes', randomize=True)
    c = Choice(question=q, text='yes')
    c = Choice(question=q, text='no')
    v = Validator(question=q, condition=yes)
    
    p = Page(branch=b)
    q = Question(page=p, qtype='free', text='Please say no')
    v = Validator(question=q, condition=no)
    
    p = Page(branch=b, randomize=True)
    q = Question(page=p, qtype='single choice', text='Please say no', randomize=True)
    c = Choice(question=q, text='yes')
    c = Choice(question=q, text='no')
    v = Validator(question=q, condition=no)
    
    q = Question(page=p, qtype='free', text='Please say yes')
    v = Validator(question=q, condition=yes)
    
    return b
    
def yes(q):
    if q.entry is None or q.entry.lower() != 'yes':
        return "Please say yes"
        
def no(q):
    if q.entry is None or q.entry.lower() != 'no':
        return "Please say no"
        
def End():
    b = Branch()
    p = Page(branch=b, terminal=True)
    q = Question(page=p, text='This is a blank page')
    return b
        
app = create_app(Config, start=Start)

@app.shell_context_processor
def make_shell_context():
	return {'db':db, 'query':query, 'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable}