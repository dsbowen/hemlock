from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question

def Start():
    b = Branch(next=End)
    p = Page(branch=b)
    q = Question(page=p, text='hello world')
    q = Question(page=p, qtype='free', text="what's your name?")
    b.set_args(q)
    p = Page(branch=b)
    q = Question(page=p, text='hello moon')
    return b
    
def End(name):
    b = Branch()
    p = Page(branch=b)
    p.set_terminal()
    # q = Question(page=p, text='thank you for taking this survey, '+name.data+'!')
    q = Question(page=p, text='you can do it!!')
    return b