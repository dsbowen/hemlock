"""Free response question"""

from hemlock.models import Question
from hemlock.question_types.html_texts import *

@Question.register(qtype='free', registration='html_compiler')
def free_compiler(question):
    classes = get_classes(question)
    label = get_label(question)
    default = get_default(question.default)
    content = FREE_INPUT.format(qid=question.id, default=default)
    return QDIV.format(classes=classes, label=label, content=content)

def get_default(default):
    if hasattr(default, 'value') and default.value is not None:
        return default.value
    return ''

@Question.register(qtype='free', registration='response_recorder')
def free_response(question, response):
    question.response = question.default = response