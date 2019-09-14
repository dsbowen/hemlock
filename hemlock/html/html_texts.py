"""Html texts for Hemlock native question types"""

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

"""Questions"""
QDIV = '''
    <div class="{classes}">
    {label}
    {content}
    </div>
'''

ERROR = '''
    <span style="color:red">{error}</span>
'''

QLABEL = '''
    <label class="w-100" for="{qid}">
    {text}
    </label>
'''

FREE_INPUT = '''
    <input type="text" class="form-control" id="{qid}" name="{qid}" value="{default}">
'''

CDIV = '''
    <div class="custom-control custom-radio">
    {input}
    {label}      
    </div>
'''

CHOICE_INPUT = '''
    <input id="{cid}" value="{cid}" name="{qid}" class="custom-control-input" type="radio" {checked}>
    '''

CHOICE_LABEL = '''
    <label class="custom-control-label w-100 choice" for="{cid}">
    {text}
    </label>
'''