"""Html compile functions for Hemlock native question types"""

from hemlock.models import Question
from hemlock.question_types.html_texts import *

def get_classes(question):
    """Get question div classes"""
    classes = 'form-group question'
    if question.error is not None:
        classes += ' error'
    return classes

def get_label(question):
    """Get question label"""
    error = question.error
    error = '' if error is None else ERROR.format(error=error)
    return QLABEL.format(qid=question.id, text=error+question.text)

@Question.register_html_compiler('embedded')
def compile_embedded(question):
    """Embedded questions are not displayed"""
    return ''

@Question.register_html_compiler('text')
def compile_text(question):
    classes = get_classes(question)
    label = get_label(question)
    return QDIV.format(classes=classes, label=label, content='')
    
@Question.register_html_compiler('free')
def compile_free(question):
    classes = get_classes(question)
    label = get_label(question)
    default = question.default
    default = '' if default is None else default
    content = FREE_INPUT.format(qid=question.id, default=default)
    return QDIV.format(classes=classes, label=label, content=content)
    
@Question.register_html_compiler('single choice')
def compile_single_choice(question):
    classes = get_classes(question)
    qlabel = get_label(question)
    
    choice_divs = []
    for c in q.choices:
        checked = 'checked' if question.default.choice == c else ''
        input = CHOICE_INPUT.format(
            cid=c.id, qid=question.id, checked=checked)
        label = CHOICE_LABEL.format(cid=c.id, text=c.text)
        choice_divs.append(CDIV.format(input=input, label=label))
    content = ''.join(choice_divs)
    
    return QDIV.format(classes=classes, label=qlabel, content=content)