"""Html texts for Hemlock native question types"""

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
    return QLABEL.format(qid=question.qid, text=error+question.text)

QDIV = """
        <div id="{qid}" class="{classes}">{label}{content}
        </div>"""

ERROR = """<span style="color:red">{error}</span>"""

QLABEL = """
            <label class="w-100" for="{qid}">
            {text}
            </label>"""

FREE_INPUT = """
            <input type="text" class="form-control" id="{qid}" name="{qid}" value="{default}">"""

"""Choices"""
def get_choice_content(question, choice_class, input_type):
    """Get the content of a choice question"""
    return ''.join([choice_div(choice, choice_class, input_type) 
        for choice in question.choices])
    
def choice_div(choice, choice_classes, input_type):
    """<div> tag for choice"""
    question = choice.question
    classes = get_choice_classes(choice_classes)
    checked = get_checked(question.default, choice)
    input = CHOICE_INPUT.format(
        cid=choice.cid, qid=question.qid, type=input_type, checked=checked)
    label = CHOICE_LABEL.format(cid=choice.cid, text=choice.text)
    return CDIV.format(classes=classes, input=input, label=label)

def get_choice_classes(classes):
    """Add custom-control to choice classes"""
    return "custom-control "+' '.join(classes)

def get_checked(default, choice):
    """Determine whether choice is the default (checked)"""
    if hasattr(default, 'choices') and choice in default.choices:
        return 'checked'
    return ''

CDIV = """
            <div class="{classes}">{input}{label}      
            </div>"""

CHOICE_INPUT = """
                <input id="{cid}" value="{cid}" name="{qid}" class="custom-control-input" type="{type}" {checked}>"""

CHOICE_LABEL = """
                <label class="custom-control-label w-100 choice" for="{cid}">
                {text}
                </label>"""