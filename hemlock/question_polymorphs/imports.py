"""Question polymorph imports"""

from hemlock.app.factory import db
from hemlock.database.models import Question

"""Question"""
def get_classes(question):
    """Get question div classes"""
    classes = 'form-group question'
    if question.error is not None:
        classes += ' error'
    return classes

def get_label(question):
    """Get question label"""
    error = question.error
    error = '' if error is None else ERROR.format(error=error)
    text = question.text if question.text is not None else ''
    return QLABEL.format(id=question.model_id, text=error+text)

QDIV = """
<div id="{id}" class="{classes}">
    {label}
    {content}
</div>
"""

ERROR = """
<span style="color:red">
    {error}
</span>
"""

QLABEL = """
<label class="w-100" for="{id}">
    {text}
</label>
"""

FREE_INPUT = """
<input type="text" class="form-control" id="{id}" name="{id}" value="{default}">
"""

"""Choices"""
def get_choice_qdiv(question, choice_class, input_type):
    """Get question <div> for choice questions"""
    classes = get_classes(question)
    qlabel = get_label(question)
    content = ''.join([choice_div(choice, choice_class, input_type) 
        for choice in question.choices])
    return QDIV.format(
        qid=question.qid, classes=classes, label=qlabel, content=content)
    
def choice_div(choice, choice_classes, input_type):
    """<div> tag for choice"""
    question = choice.question
    classes = 'custom-control '+' '.join(choice_classes)
    checked = get_checked(question.default, choice)
    input = CHOICE_INPUT.format(
        cid=choice.cid, qid=question.qid, type=input_type, checked=checked)
    label = CHOICE_LABEL.format(cid=choice.cid, text=choice.text)
    return CDIV.format(classes=classes, input=input, label=label)

def get_checked(default, choice):
    """Determine whether choice is the default (checked)
    
    For multi choice, default is a list of choices. For single choice, 
    default is a choice.
    """
    if isinstance(default, list):
        default = [choice.id for choice in default]
        return 'checked' if choice.id in default else ''
    return 'checked' if choice == default else ''

CDIV = """
            <div class="{classes}">{input}{label}      
            </div>"""

CHOICE_INPUT = """
                <input id="{cid}" value="{cid}" name="{qid}" class="custom-control-input" type="{type}" {checked}>"""

CHOICE_LABEL = """
                <label class="custom-control-label w-100 choice" for="{cid}">
                {text}
                </label>"""