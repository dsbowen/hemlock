"""Html texts for Hemlock native question types"""

"""Page"""
PAGE_ID = '''
    <page id="p{pid}"/>
'''

"""Navigation"""
BREAK = '''
    <br>
'''

FORWARD_BUTTON = '''
    <button id="forward-button" name="direction" type="submit" class="btn btn-outline-primary" style="float: right;" value="forward">
    >> 
    </button>
'''

BACK_BUTTON = '''
    <button id="back-button" name="direction" type="submit" class="btn btn-outline-primary" style="float: left;" value="back"> 
    << 
    </button>
'''

PAGE_BREAK = '''
    <br style="line-height:3;"></br>
'''

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
    return QLABEL.format(qid=question.id, text=error+question.text)

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
    <label class="w-100" for="q{qid}">
    {text}
    </label>
'''

FREE_INPUT = '''
    <input type="text" class="form-control" id="q{qid}" name="q{qid}" value="{default}">
'''

CDIV = '''
    <div class="custom-control custom-radio">
    {input}
    {label}      
    </div>
'''

CHOICE_INPUT = '''
    <input id="c{cid}" value="c{cid}" name="q{qid}" class="custom-control-input" type="radio" {checked}>
    '''

CHOICE_LABEL = '''
    <label class="custom-control-label w-100 choice" for="c{cid}">
    {text}
    </label>
'''