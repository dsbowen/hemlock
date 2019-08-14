##############################################################################
# Default html compiler functions
# by Dillon Bowen
# last modified 08/14/2019
##############################################################################

from hemlock.factory import compiler
from hemlock.compiler.html_texts import *

# Compile embedded data
@compiler.register('embedded')
def compile_embedded(q):
    return ''

# Compile text question
@compiler.register('text')
def compile_text(q):
    classes = get_classes(q)
    label = get_label(q)
    return QDIV.format(classes=classes, label=label, content='')
    
# Compile free response question
@compiler.register('free')
def compile_free(q):
    classes = get_classes(q)
    label = get_label(q)
    default = q.get_default()
    default = '' if default is None else default
    content = FREE_INPUT.format(qid=q.id, default=default)
    return QDIV.format(classes=classes, label=label, content=content)
    
# Compile single choice question
@compiler.register('single choice')
def compile_single_choice(q):
    classes = get_classes(q)
    qlabel = get_label(q)
    
    choices = q.get_choices()
    [c._set_checked(c.id==q._default) for c in choices]
    choice_divs = []
    for c in choices:
        input = CHOICE_INPUT.format(cid=c.id, qid=q.id, checked=c._checked)
        label = CHOICE_LABEL.format(cid=c.id, text=c.get_text())
        choice_divs.append(CDIV.format(input=input, label=label))
    content = ''.join(choice_divs)
    
    return QDIV.format(classes=classes, label=qlabel, content=content)
    
# Get question div classes
def get_classes(q):
    classes = 'form-group question'
    if q.get_error() is not None:
        classes += 'error'
    return classes

# Get question label
def get_label(q):
    error = q.get_error()
    error = '' if error is None else error
    return QLABEL.format(qid=q.id, text=error+q.get_text())