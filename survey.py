###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock.query import query
from hemlock.models.participant import Participant
from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question

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

# def Start():
    # b = Branch(next=greeting)
    
    # p = Page(branch=b)
    # q = Question(page=p, text='Halt! Who goes there?', qtype='free', var='name', all_rows=True)
    # b.set_args(q.id)
    
    # return b
    
# def integer(n):
    # return n.isdigit()
    
# def g(n):
    # if not n.isdigit():
        # return True
    # return int(n)>2
    
# def empty(d):
    # return d is not None
    
# def greeting(name_id):
    # name = query(name_id).data
    
    # b = Branch(next=goodbye)
    
    # p = Page(branch=b)
    # q = Question(page=p, text='Oh, hey {0}!!'.format(name))
    
    # p = Page(branch=b)
    # q = Question(page=p, text='So I figured out how to program multiple choice questions today :)')
    # q = Question(page=p, var='awesome', qtype='single choice')
    # q.set_text('How awesome is that?')
    # q.add_choice('pretty awesome')
    # q.add_choice('super awesome')
    # q.add_choice('super duper awesome')
    # q.add_validation(condition=empty, message='ANSWER THE QUESTION!!')
    # q.set_randomize()
    
    # b.set_args(q.id)
    
    # q = Question(page=p, var='integer', qtype='free', text="What's your favorite integer greater than 2?")
    # q.add_validation(condition=integer, message='I said an INTEGER!')
    # q.add_validation(condition=g, message='I said GREATER THAN 2!')
    
    # return b
    
# def goodbye(awesome_id):
    # awesome = str(query(awesome_id).data)
    
    # b = Branch()
    # p = Page(branch=b, terminal=True)
    # q = Question(page=p, text="Indeed, it is {0}, isn't it?".format(awesome))
    # q = Question(page=p, text='Goodnight my dear xx')
    
    # return b

##This is the first navigation function
# def Start():
    # b = Branch(next=Thanks)
    
    ##embedded data is inserted to the branch, not to a page
    # condition = Question(branch=b, var='condition', data='control', all_rows=True)
    
    ##the first page
    # p = Page(branch=b)
    # q = Question(page=p, text='Welcome to Hemlock!')
    # q = Question(page=p, text="Let's start with some simple free response questions.")
    
    ##second page contains free response questions
    # p = Page(branch=b)
    # first = Question(page=p, var='first_name', qtype='free', all_rows=True)
    # first.set_text("What's your first name?")
    # last = Question(page=p, var='last_name', qtype='free', all_rows=True)
    # last.set_text("...and your last name?")
    
    ##set arguments for next navigation function
    # b.set_args({'first':first.id, 'last':last.id})
    
    # return b
    
##creates a question asking about ice cream
# def ice_cream(page, index):
    # q = Question(page=page, var='ice_cream', qtype='free')
    # q.set_text('Favorite ice cream number '+str(index))

##the second navigation function
# def Thanks(name_ids):
    # b = Branch(next=FirstEst)
    
    ##demonstrates how to query and use participant responses
    # p = Page(branch=b)
    # name = query(name_ids)
    # q = Question(page=p, text='Thanks for taking this survey, '+name['first'].data+' '+name['last'].data+'!')
    # q = Question(page=p, text="Let's continue to some more simple free response questions.")
    
    ##convenient looping to create multiple, similar questions
    # p = Page(branch=b)
    # q = Question(page=p, text="Alright, now, what are your three favorite flavors of ice cream?")
    # for i in range(3):
        # ice_cream(p, i+1)
    
    # return b
    
# def FirstEst():
    # b = Branch()
    
    ##demonstration of page branching
    # p = Page(branch=b, next=SecondEst)
    # q = Question(page=p, var='first_est', qtype='free', text='Please make your first estimate')
    # p.set_args(q.id)
    
    ##set terminal to True for the last page of the survey
    # p = Page(branch=b, terminal=True)
    # q = Question(page=p, text="Thank you for taking my survey!")
    
    # return b
    
# def SecondEst(first_est_id):
    # b = Branch()
    
    # p = Page(branch=b)
    # first_est = query(first_est_id).data
    # q = Question(page=p, text='Your first estimate was '+str(first_est))
    # q = Question(page=p, var='second_est', qtype='free', text='Please make your second estimate.')
    
    # return b