###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock import create_app, db, query, Participant, Branch, Page, Question, Choice, Validator, Variable
from config import Config

def Start():
    b = Branch(next=IceCream)
    
    p = Page(branch=b)
    name = Question(page=p, var='name', qtype='free', all_rows=True)
    name.set_text("Hey there, what's your name?")
    v = Validator(question=name, condition=not_empty, args="I ASKED YOU A QUESTION!")
    
    p = Page(branch=b)
    q = Question(page=p, render=greet, render_args=name.id)
    
    return b
    
def not_empty(q, message):
    if not bool(q.entry):
        return message
    
def greet(q, name_id):
    name = query(name_id).entry
    q.set_text('Hello, {0}!'.format(name))
    
def IceCream():
    b = Branch()
    
    p = Page(branch=b)
    ice_cream = Question(page=p, var='ice_cream', qtype='single choice', randomize=True)
    ice_cream.set_text("What's your favorite ice cream?")
    c = Choice(question=ice_cream, text='chocolate')
    c = Choice(question=ice_cream, text='orange')
    c = Choice(question=ice_cream, text='lavender')
    v = Validator(question=ice_cream, condition=not_empty, args='ANSWER THE QUESTION!')
    
    p = Page(branch=b)
    q = Question(page=p, qtype='single choice', render=verify, render_args=ice_cream.id)
    c = Choice(question=q, text='yes', value=1)
    c = Choice(question=q, text='no', value=0)
    v = Validator(question=q, condition=not_empty, args='Please answer the question.')
    p.set_next(RepeatOnNonverified, q.id)
    
    return b

def verify(q, ice_cream_id):
    ice_cream = query(ice_cream_id)
    selected = ice_cream.get_selected()[0].text
    nonselected = [x.text for x in ice_cream.get_nonselected()]
    q.set_text('''
        You said you prefer {0} over {1} and {2}. Is this correct?
        '''.format(selected, nonselected[0], nonselected[1]))
        
def RepeatOnNonverified(verified_id):
    verified = int(query(verified_id).data)
    if verified:
        return AttentionCheck()
    else:
        return IceCream()
    
def AttentionCheck():
    b = Branch()
    
    p = Page(branch=b)
    attn = Question(page=p, var='attn', qtype='free', all_rows=True, post=pass_fail)
    attn.set_text('''
        Please enter 99 in the text box. This is an attention check.
        ''')
        
    p = Page(branch=b, terminal=True)
    q = Question(page=p, render=disp_pass_fail, render_args=attn.id)
    
    return b
    
def pass_fail(attn):
    attn.set_data(attn.entry=='99')
    
def disp_pass_fail(q, attn_id):
    attn = query(attn_id)
    if attn.data:
        q.set_text('Congratulations! You entered {0} and passed the attention check!!'.format(attn.entry))
    else:
        q.set_text('You entered {0} and FAILED the attention check!!'.format(attn.entry)) 

app = create_app(Config, start=Start)

@app.shell_context_processor
def make_shell_context():
	return {'db':db, 'query':query, 'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable}