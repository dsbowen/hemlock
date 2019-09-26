"""Embedded data"""

from hemlock.database.models import Question

@Question.register(type='embedded', registration='html_compiler')
def embedded_compiler(question):
    return ''

@Question.register(type='embedded', registration='response_recorder')
def embedded_response(question, response):
    return

@Question.register(type='embedded', registration='data_recorder')
def embedded_data(question):
    return