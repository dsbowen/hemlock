from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question

def Start():
    b = Branch(next=End)
    p = Page(branch=b)
    q1 = Question(page=p, text='hello world')
    q2 = Question(page=p, qtype='free', text="what's your name?")
    b.set_args(q2.id)
    p = Page(branch=b)
    q = Question(page=p, text='hello moon')
    return b
    
def End(name_id):
    name = Question.query.get(name_id)
    b = Branch()
    p = Page(branch=b)
    p.set_terminal()
    q = Question(page=p, text='thank you for taking this survey, '+name.data+'!')
    return b