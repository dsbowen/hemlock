"""Multiple choice question"""

from hemlock.database.models import Question
from hemlock.question_types.html_texts import *

@Question.register(qtype='multi choice', registration='html_compiler')
def multi_choice_compiler(question):
    return get_choice_qdiv(
        question, choice_class=['custom-checkbox'], input_type='checkbox')

@Question.register(qtype='multi choice', registration='response_recorder')
def multi_choice_response(question, choice_cids):
    selected, nonselected = [], []
    for choice in question.choices:
        if choice.cid in choice_cids:
            selected.append(choice)
        else:
            nonselected.append(choice)
    question.response = selected.copy()
    question.default = selected.copy()
    question.selected_choices = selected.copy()
    question.nonselected_choices = nonselected
    
@Question.register(qtype='multi choice', registration='data_recorder')
def multi_choice_data(question):
    data = {}
    for choice in question.choices:
        data[choice.value] = int(choice in question.response)
    question.data = data

@Question.register(qtype='multi choice', registration='data_packer')
def multi_choice_pack(question):
    var = question.var
    return {var+key: question.data[key] for key in question.data.keys()}