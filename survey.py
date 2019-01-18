from hemlock.models.branch import Branch
from hemlock.models.page import Page
from hemlock.models.question import Question

def start():
	b = Branch()
	p = Page(branch=b)
	q = Question(page=p, text='hello world')
	return b
	
def end():
	return 'thank you!'