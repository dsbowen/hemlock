###############################################################################
# Html compiler functions
# by Dillon Bowen
# last modified 03/19/2019
###############################################################################

from random import choice
from string import ascii_letters, digits



###############################################################################
# Page general html
###############################################################################

# Create a hidden tag for form (for security purposes)
def hidden_tag():
    return '''
    <div class='form-group'
        <input name='crsf_token' type='hidden' value='{0}'>
    </div>
    '''.format(''.join([choice(ascii_letters + digits) for i in range(90)]))
    
# Submit button
def submit(page):
    html = '<br></br>'
    if page._back:
        html += '''
    <button name='direction' type='submit' class='btn btn-primary' style='float: left;' value='back'> 
    << 
    </button>
    '''
    if page._terminal:
        return html+"<br style = 'line-height:3;'></br>"
    return html + '''
    <button name='direction' type='submit' class='btn btn-primary' style='float: right;' value='forward'>
    >> 
    </button>
    <br style = 'line-height:3;'></br>
    '''
    
    
    
###############################################################################
# Question html
###############################################################################

# Compile errors and text as question label
def compile_label(q):
    error = ''
    if q._error:
        error = '''
            <div style='color: #ff0000;'>
            {0}
            </div>
        '''.format(q._error)
    return '''
            <label for='{0}'>
            {1}
            </label>
    '''.format(q.id, error+q._text)
    
# Text question (no response)
def compile_text(q):
    return '''
    <div class='form-group'>
        {0}
    </div>    
    '''.format(compile_label(q))
    
# Free response
def compile_free(q):
    default = q._default if q._default is not None else ''
    return '''
    <div class='form-group'>
        {0}
        <input name='{1}' type='text' class='form-control' value='{2}'>
    </div>
    '''.format(compile_label(q), q.id, default)
    
# Single choice
def compile_single_choice(q):
    [c._set_checked(c.id==q._default) for c in q._choices]
    text_html = '''
    <div class='form-group'>
        {0}
    </div>
    '''.format(compile_label(q))
    choice_html = ['''
    <div class='form-check'>
        <label><input type='radio' name='{0}' value='{1}' {2}>
        {3}
        </label>
    </div>
    '''.format(q.id, c.id, c._checked, c._text) for c in q._choices]
    return ''.join([text_html]+choice_html+['<br></br>'])
    
# Dropdown
def compile_dropdown(q):
    text_html = '''
    <div class='form-group'>
        {0}
    </div>
    '''.format(compile_label(q))
    choice_html = ['''
            <a class='dropdown-item' href='#'>{0}</a>
    '''.format(c._text) for c in q._choices]
    dropdown_html = '''
    <div class='dropdown'>
        <button class='btn btn-primary dropdown-toggle' type='button' data-toggle='dropdown'>
        Dropdown Example
        </button>
        <div class='dropdown-menu'>
        {0}
        </div>
    </div>
    '''.format(''.join(choice_html))
    return text_html + dropdown_html