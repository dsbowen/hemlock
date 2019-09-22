"""Multiple choice question"""

from hemlock.database.models import Question
from hemlock.question_types.html_texts import *

@Question.register(qtype='multi choice', registration='html_compiler')
def multi_choice_compiler(question):
    classes = get_classes(question)
    qlabel = get_label(question)
    choice_class, input_type = ["custom-checkbox"], "checkbox"
    content = get_choice_content(question, choice_class, input_type)
    return QDIV.format(
        qid=question.qid, classes=classes, label=qlabel, content=content)

@Question.register(qtype='multi choice', registration='response_recorder')
def multi_choice_response(question, choice_cids):
    if not choice_cids:
        question.default.choices = []
        return
    selected, nonselected = [], []
    for choice in question.choices:
        if choice.cid in choice_cids:
            selected.append(choice)
        else:
            nonselected.append(choice)
    question.response = selected.copy()
    question.default.choices = selected.copy()
    question.selected_choices = selected.copy()
    question.nonselected_choices = nonselected

@Question.register(qtype='multi choice', registration='data_packer')
def multi_choice_pack(question):
    selected_ids = [choice.id for choice in question.data]
    return {question.var+choice.label: int(choice.id in selected_ids)
        for choice in question.choices}