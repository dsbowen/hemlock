"""Single choice question"""

from hemlock.models import Question
from hemlock.question_types.html_texts import *

@Question.register(qtype='single choice', registration='html_compiler')
def single_choice_compiler(question):
    classes = get_classes(question)
    qlabel = get_label(question)
    content = ''.join([
        choice_div(question, choice) for choice in question.choices])
    return QDIV.format(classes=classes, label=qlabel, content=content)
    
def choice_div(question, choice):
    """<div> tag for choice"""
    checked = get_checked(question.default, choice)
    input = CHOICE_INPUT.format(
        cid=choice.id, qid=question.id, checked=checked)
    label = CHOICE_LABEL.format(cid=choice.id, text=choice.text)
    return CDIV.format(input=input, label=label)

def get_checked(default, choice):
    """Determine whether choice is the default (checked)"""
    if hasattr(default, 'choice') and default.choice == choice:
        return 'checked'
    return ''

@Question.register(qtype='single choice', registration='response_recorder')
def single_choice_response(question, response):
    """Record response for a single choice question type
    
    If participant did not select a choice, set default to None and return.
    Otherwise:
    1. Get the choice id (the input choice id is 'c<id>')
    2. Set question response to the value of the selected choice
    3. Set the default choice to the selected choice
    4. Update selected and nonselected choices
    """
    if choice_id is None:
        question.default.choice = None
        return
    choice_id = choice_id[1:]
    for choice in question.choices:
        if choice.id == choice_id:
            response = choice.value
            break
    question.response = response
    question.default.choice = choice
    question.selected_choices = [choice]
    question.nonselected_choices = [
        c for c in question.choices if c != choice]