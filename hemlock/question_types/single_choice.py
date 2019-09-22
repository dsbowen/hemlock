"""Single choice question"""

from hemlock.database.models import Question
from hemlock.question_types.html_texts import *

@Question.register(qtype='single choice', registration='html_compiler')
def single_choice_compiler(question):
    classes = get_classes(question)
    qlabel = get_label(question)
    choice_class, input_type = ["custom-radio"], 'radio'
    content = get_choice_content(question, choice_class, input_type)
    return QDIV.format(
        qid=question.qid, classes=classes, label=qlabel, content=content)

@Question.register(qtype='single choice', registration='response_recorder')
def single_choice_response(question, choice_cid):
    """Record response for a single choice question type
    
    If participant did not select a choice, set default to None and return.
    Otherwise:
    1. Set question response to the value of the selected choice
    2. Set the default choice to the selected choice
    3. Update selected and nonselected choices
    """
    if not choice_cid:
        question.default.choices = []
        return
    choice_cid = choice_cid[0]
    for choice in question.choices:
        if choice.cid == choice_cid:
            selected = choice
            break
    question.response.value = selected.value
    question.default.choices = [selected]
    question.selected_choices = [selected]
    question.nonselected_choices = [
        c for c in question.choices if c != selected]