###############################################################################
# Example Hemlock survey
# by Dillon Bowen
# last modified 01/21/2019
###############################################################################

from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question

def Start():
    b = Branch(next=IceCream)
    p = Page(branch=b)
    q = Question(page=p, text='Welcome to Hemlock')
    first_name = Question(page=p, var='first_name', qtype='free', text="What's your first name?", all_rows=True)
    last_name = Question(page=p, var='last_name', qtype='free', text="What's your last name?", all_rows=True)
    b.set_args([first_name.id, last_name.id])
    return b
    
def IceCream(args):
    first_id, last_id = args
    first_name, last_name = Question.query.filter(Question.id.in_(args))
    
    b = Branch(next=End)
    p = Page(branch=b)
    q = Question(page=p, text='Welcome, '+first_name.data+' '+last_name.data+'!')
    q = Question(page=p, text='What are your three favorite flavors of ice cream?')
    for i in range(3):
        q = Question(page=p, var='ice_cream', qtype='free')
    p = Page(branch=b)
    q = Question(page=p, var='cereal', qtype='free', text='What is your favorite cereal?')
    return b
    
def End():
    b = Branch()
    p = Page(branch=b)
    p.set_terminal()
    q = Question(page=p, text='Thank you for taking this survey!!')
    return b