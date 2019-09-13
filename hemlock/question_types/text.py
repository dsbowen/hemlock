"""Text question"""

from hemlock.models import Question
from hemlock.question_types.html_texts import *

@Question.register(qtype='text', registration='html_compiler')
def text_compiler(question):
    classes = get_classes(question)
    label = get_label(question)
    return QDIV.format(classes=classes, label=label, content='')

@Question.register(qtype='text', registration='response_recorder')
def text_response(question, response):
    return

@Question.register(qtype='text', registration='data_recorder')
def text_data(question):
    return