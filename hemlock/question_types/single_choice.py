"""Single choice question"""

from hemlock.database.models import Question
from hemlock.question_types.html_texts import *

@Question.register(qtype='single choice', registration='html_compiler')
def single_choice_compiler(question):
    return get_choice_qdiv(
        question, choice_class=['custom-radio'], input_type='radio')

@Question.register(qtype='single choice', registration='response_recorder')
def single_choice_response(question, choice_cid):
    """Record response for a single choice question type
    
    If participant did not select a choice, set default to None and return.
    Otherwise:
    1. Set question response to the value of the selected choice
    2. Set the default choice to the selected choice
    3. Update selected and nonselected choices
    """
    if choice_cid:
        choice_cid = choice_cid[0]
        for choice in question.choices:
            if choice.cid == choice_cid:
                selected = choice
                break
    else:
        selected = None    
    question.response = question.default = selected
    question.selected_choices = [] if selected is None else [selected]
    question.nonselected_choices = [
        c for c in question.choices if c != selected]

@Question.register(qtype='single choice', registration='data_recorder')
def single_choice_data(question):
    response = question.response
    question.data = None if response is None else response.value