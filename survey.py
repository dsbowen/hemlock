"""Hemlock survey"""

from hemlock import *
from texts import *
from flask_login import current_user
    
def Start(root=None):
    b = Branch()
    p = Page(b, timer_var='v1', all_rows=True)
    q = Question(p, qtype='free', text='name', var='Name', all_rows=True)
    q = Question(p, qtype='single choice', text='ice cream 1', var='IceCream')
    c = Choice(q, text='Chocolate')
    c = Choice(q, text='Vanilla')
    q = Question(p, qtype='single choice', text='ice cream 2', var='IceCream')
    c = Choice(q, text='Strawberry')
    c = Choice(q, text='Cookies and Cream')
    
    p = Page(b, terminal=True)
    q = Question(p, text='goodbye moon')
    return b