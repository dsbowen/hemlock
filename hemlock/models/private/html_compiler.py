##############################################################################
# Html compiler functions
# by Dillon Bowen
# last modified 07/21/2019
##############################################################################

from hemlock.models.private.html_texts import *
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
# Question html
##############################################################################

# Compile question
def compile_question(q):
    div_class = 'form-group question'
    if q.get_error() is not None:
        div_class += ' error'
    return QUESTION.format(div_class, compile_div(q))
    
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
    return ''.join([CHOICE.format(q.id, c.id, c._checked, c.get_text()) 
        for c in choices])
