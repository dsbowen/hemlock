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

def Start():
    b = Branch(next=greeting)
    
    p = Page(branch=b)
    q = Question(page=p, text='Halt! Who goes there?', qtype='free', var='name', all_rows=True)
    b.set_args(q.id)
    
    return b
    
def greeting(name_id):
    name = query(name_id).data
    
    b = Branch(next=goodbye)
    
    p = Page(branch=b)
    q = Question(page=p, text='Oh, hey {0}!!'.format(name))
    
    p = Page(branch=b)
    q = Question(page=p, text='So I figured out how to program multiple choice questions today :)')
    q = Question(page=p, var='awesome', qtype='single choice')
    q.set_text('How awesome is that?')
    q.add_choice('pretty awesome')
    q.add_choice('super awesome')
    q.add_choice('super duper awesome')
    # q.set_randomize()
    
    b.set_args(q.id)
    
    return b
    
def goodbye(awesome_id):
    awesome = str(query(awesome_id).data)
    
    b = Branch()
    p = Page(branch=b, terminal=True)
    q = Question(page=p, text='Indeed, it is '+awesome+", isn't it?")
    q = Question(page=p, text='Goodnight my dear xx')
    
    return b

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