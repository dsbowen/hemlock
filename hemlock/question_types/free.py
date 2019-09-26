"""Free response question"""

from hemlock.database.models import Question
from hemlock.question_types.html_texts import *

@Question.register(type='free', registration='html_compiler')
def free_compiler(question):
    classes = get_classes(question)
    label = get_label(question)
    default = question.default or ''
    content = FREE_INPUT.format(qid=question.qid, default=default)
    return QDIV.format(
        qid=question.qid, classes=classes, label=label, content=content)

@Question.register(type='free', registration='response_recorder')
def free_response(question, response):
    response = None if not response else response[0]
    question.response = question.default = response