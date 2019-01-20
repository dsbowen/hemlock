from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question

def Start():
    b = Branch(next=End)
    p = Page(branch=b)
    q = Question(page=p, text='hello world')
    q = Question(page=p, qtype='free', text="what's your name?")
    p = Page(branch=b)
    q = Question(page=p, text='hello moon')
    return b
    
def End():
    b = Branch()
    p = Page(branch=b)
    p.set_terminal()
    q = Question(page=p, text='thank you!')
    return b