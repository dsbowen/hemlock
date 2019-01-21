from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question

def Start():
    b = Branch(next=End)
    p1 = Page(branch=b)
    q = Question(page=p1, text='hello world')
    q1 = Question(page=p1, var='name', qtype='free', text="what's your first name?")
    q2 = Question(page=p1, var='name', qtype='free', text="what's your last name?")
    b.set_args([q1.id, q2.id])
    # p = Page(branch=b)
    # q = Question(page=p, text='hello moon')
    # p1.assign_branch(b)
    return b
    
def End(args):
    first_id, last_id = args
    first, last = Question.query.get(first_id), Question.query.get(last_id)
    b = Branch()
    p = Page(branch=b)
    p.set_terminal()
    q = Question(page=p, text='thank you for taking this survey, '+first.data+' '+last.data+'!')
    return b