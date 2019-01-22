###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question

def Start():
    b = Branch(next=Thanks)
    
    p = Page(branch=b)
    q = Question(page=p, text='Welcome to Hemlock!')
    q = Question(page=p, text="Let's start with some simple free response questions.")
    
    p = Page(branch=b)
    first = Question(page=p, var='first_name', qtype='free', all_rows=True)
    first.set_text("What's your first name?")
    last = Question(page=p, var='last_name', qtype='free', all_rows=True)
    last.set_text("...and your last name?")
    
    b.set_args([first.id, last.id])
    
    return b
    
def ice_cream(page, index):
    q = Question(page=page, var='ice_cream', qtype='free')
    q.set_text('Favorite ice cream number '+str(index))

def Thanks(name_ids):
    b = Branch()
    
    p = Page(branch=b)
    first, last = Question.query.filter(Question.id.in_(name_ids))
    q = Question(page=p, text='Thanks for taking this survey, '+first.data+' '+last.data+'!')
    q = Question(page=p, text="Let's continue to some more simple free response questions.")
    
    p = Page(branch=b)
    q = Question(page=p, text="Alright, now, what are your three favorite flavors of ice cream?")
    for i in range(3):
        ice_cream(p, i+1)
        
    p = Page(branch=b, terminal=True)
    q = Question(page=p, text="Thank you for taking my survey!")
    
    return b