"""Single choice question"""

from hemlock.database.models import Question
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
        cid=choice.cid, qid=question.qid, checked=checked)
    label = CHOICE_LABEL.format(cid=choice.cid, text=choice.text)
    return CDIV.format(input=input, label=label)

def get_checked(default, choice):
    """Determine whether choice is the default (checked)"""
    if hasattr(default, 'choice') and default.choice == choice:
        return 'checked'
    return ''

@Question.register(qtype='single choice', registration='response_recorder')
def single_choice_response(question, choice_cid):
    """Record response for a single choice question type
    
    If participant did not select a choice, set default to None and return.
    Otherwise:
    1. Set question response to the value of the selected choice
    2. Set the default choice to the selected choice
    3. Update selected and nonselected choices
    """
    if choice_cid is None:
        question.default.choice = None
        return
    for choice in question.choices:
        if choice.cid == choice_cid:
            selected = choice
            break
    question.response = selected.value
    question.default.choice = selected
    question.selected_choices = [selected]
    question.nonselected_choices = [
        c for c in question.choices if c != selected]