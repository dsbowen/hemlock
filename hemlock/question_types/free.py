"""Free response question"""

from hemlock.database.models import Question
from hemlock.question_types.html_texts import *

@Question.register(qtype='free', registration='html_compiler')
def free_compiler(question):
    classes = get_classes(question)
    label = get_label(question)
    default = get_default(question.default)
    content = FREE_INPUT.format(qid=question.qid, default=default)
    return QDIV.format(
        qid=question.qid, classes=classes, label=label, content=content)

def get_default(default):
    if hasattr(default, 'value') and default.value is not None:
        return default.value
    return ''

@Question.register(qtype='free', registration='response_recorder')
def free_response(question, response):
    response = None if response == '' else response
    question.response = question.default.value = response