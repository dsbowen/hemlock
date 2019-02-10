###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock import create_app, db, query, Participant, Branch, Page, Question, Choice, Validator, Variable
from config import Config

def Start():
    b = Branch()
    
    p = Page(branch=b)
    q = Question(page=p, text='(Try leaving this question blank)')
    name = Question(page=p, var='name', qtype='free', text="Hey there, what's your name?")
    v = Validator(question=name, condition=not_empty, args="I ASKED YOU A QUESTION!")
    
    p = Page(branch=b)
    greet = Question(page=p, render=greeting, render_args=name.id)
    q = Question(page=p, var='ice_cream', qtype='single choice')
    q.set_text("What's your favorite flavor ice cream?")
    c = Choice(question=q, text='chocolate')
    c = Choice(question=q, text='vanilla')
    c = Choice(question=q, text='strawberry')
    v = Validator(question=q, condition=not_empty, args='Please answer the question.')
    v = Validator(question=q, condition=not_strawberry)
    
    p = Page(branch=b, post=check_attn)
    attn = Question(page=p, var='attention', qtype='free', text='Please enter 99')
    
    p = Page(branch=b, terminal=True)
    q = Question(page=p, render=pass_fail, render_args=attn.id)
    
    return b
    
def greeting(q, name_id):
    name = query(name_id).data
    q.set_text('Hello, {0}!'.format(name))
    
def not_empty(question, message):
    if not bool(question.data):
        return message
        
def not_strawberry(q):
    if q.data=='strawberry':
        return "Strawberry is objectively a terrible ice cream flavor. Try again."
    
def check_attn(p):
    q = p.questions[0]
    q.set_data(int(q.data=='99'))

def pass_fail(q, attn_id):
    passed = query(attn_id).data
    if passed:
        q.set_text('Congratulations! You passed the attention check!')
    else:
        q.set_text('You have FAILED the attention check!')

app = create_app(Config, start=Start)

@app.shell_context_processor
def make_shell_context():
	return {'db':db, 'query':query, 'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable}