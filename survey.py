from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question

def Start():
    b = Branch(next=End)
    p1 = Page(branch=b)
    q = Question(page=p1, text='hello world')
    q = Question(page=p1, var='name', qtype='free', text="what's your name?")
    b.set_args(q.id)
    # p = Page(branch=b)
    # q = Question(page=p, text='hello moon')
    # p1.assign_branch(b)
    return b
    
def End(name_id):
    name = Question.query.get(name_id)
    b = Branch()
    p = Page(branch=b)
    p.set_terminal()
    q = Question(page=p, text='thank you for taking this survey, '+name.data+'!')
    return b