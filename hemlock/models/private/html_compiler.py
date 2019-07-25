##############################################################################
# Html compiler functions
# by Dillon Bowen
# last modified 07/24/2019
##############################################################################

from hemlock.models.private.html_texts import *
from flask import current_app
from random import choice



##############################################################################
# Navigation
##############################################################################
    
# Submit button
def submit(page):
    html = BREAK
    if page._back:
        html += BACK_BUTTON
    if not page._terminal:
        html += FORWARD_BUTTON
    return html + PAGE_BREAK    


    
##############################################################################
# Page html
##############################################################################

# Page debug html
def compile_page(p):
    return PAGE_DEBUG.format(*get_debug_attrs(p))
    
# Debugging html attributes
def get_debug_attrs(object):
    if not current_app.debug_mode:
        return ('','','')
    debug = object.get_debug()
    debug = '' if debug is None else debug.__name__
    args = object.get_debug_args()
    args = '' if args is None else str(args)
    attrs = object.get_debug_attrs()
    attrs = '' if attrs is None else str(attrs)
    return (debug, args, attrs)



##############################################################################
# Question html
##############################################################################

# Compile question
def compile_question(q):
    div_class = 'form-group question'
    if q.get_error() is not None:
        div_class += ' error'
    return QUESTION.format(div_class, *get_debug_attrs(q), compile_div(q))
    
# Compile form-group div
def compile_div(q):
    error = q.get_error()
    error = '' if error is None else ERROR.format(error)    
    return DIV.format(q.id, error+q.get_text(), compile_by_type(q))
    
# Compile question by question type
def compile_by_type(q):
    qtype = q.get_qtype()
    if qtype == 'free':
        return free(q)
    if qtype == 'single choice':
        return single_choice(q)
    return ''
    
# Compile for free response question
def free(q):
    default = q.get_default()
    default = '' if default is None else default
    return FREE.format(q.id, default)
    
# Compile for single choice question
def single_choice(q):
    [c._set_checked(c.id==q._default) for c in q._choices]
    choices = q.get_choices()
    return ''.join([CHOICE.format(*get_choice_args(q, c)) for c in choices])

# Get arguments for choice html
def get_choice_args(q, c):
    return (q.id, c.id, c._checked, *get_debug_attrs(c), c.get_text()) 
