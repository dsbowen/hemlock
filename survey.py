###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock import create_app, db, query, Participant, Branch, Page, Question, Choice, Validator, Variable
from config import Config

def not_empty(question, message):
    if not bool(question.data):
        return message

def Start():
    b = Branch(next=greeting)
    
    p = Page(branch=b)
    q = Question(page=p, text='''
        <p>So... I didn't get around to making the back button :(</p>
        <p>I thought it would be a good idea to be able to validate question responses first.</p>''')
    
    p = Page(branch=b)
    q = Question(page=p, text='(Try leaving this question blank)')
    q = Question(page=p, var='name', qtype='free', text="Hey there, what's your name??")
    q.add_validation(not_empty, "I ASKED YOU A QUESTION!!!")
    
    b.set_args(q.id)
    
    return b
    
def love_you(question):
    if question.data is not None and not int(question.data):
        return "I'm sorry, your answer was incorrect. Please try again."
    
def greeting(name_id):
    name = query(name_id).data
    
    b = Branch()
    
    p = Page(branch=b)
    q = Question(page=p, text="Oh, hey {0}! You have such a pretty name. I don't know if I ever told you that before.".format(name))
    
    q = Question(page=p, var='love_you', qtype='single choice')
    q.set_text("Do you know how much I love you? (Try clicking 'not very much' or leaving it blank)")
    q.add_choice(text='mmm, not very much...', value=0)
    q.add_choice(text='a whole hell of a lot', value=1)
    q.add_validation(not_empty, "Oh no, please give me an answer!")
    q.add_validation(love_you)
    
    p = Page(branch=b, terminal=True)
    q = Question(page=p, text="Goodnight my dear. I adore you xx")
    
    return b

app = create_app(Config, start=Start)

@app.shell_context_processor
def make_shell_context():
	return {'db':db, 'query':query, 'Participant':Participant, 'Branch':Branch, 'Page':Page, 'Question':Question, 'Choice':Choice, 'Validator':Validator, 'Variable':Variable}