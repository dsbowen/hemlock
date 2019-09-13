"""Embedded data"""

from hemlock.models import Question

@Question.register(qtype='embedded', registration='html_compiler')
def embedded_compiler(question):
    return ''

@Question.register(qtype='embedded', registration='response_recorder')
def embedded_response(question, response):
    return

@Question.register(qtype='embedded', registration='data_recorder')
def embedded_data(question):
    return