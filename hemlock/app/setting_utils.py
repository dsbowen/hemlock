"""Miscellaneous default settings texts and functions"""

TIME_EXPIRED = """You have exceeded your time limit for this survey."""

RESTART = """
<p>Click << to return to your in progress survey. Click >> to restart the survey.</p>
<p>If you choose to restart the survey, your responses will not be saved.</p>
"""

SCREENOUT = """
<p>Our records indicate that you have already participated in this or similar surveys.</p>
<p>Thank you for your continuing interest in our research.</p>
"""

BACK_BUTTON_TEMPLATE = """
<button id="back-button" name="direction" type="submit" class="{classes} btn btn-outline-primary" style="float: left;" value="back"> 
    {text}
</button>
"""

BACK_BUTTON = BACK_BUTTON_TEMPLATE.format(classes='', text='<<')

FORWARD_BUTTON_TEMPLATE = """
<button id="forward-button" name="direction" type="submit" class="{classes} btn btn-outline-primary" style="float: right;" value="forward">
    {text}
</button>
"""

FORWARD_BUTTON = FORWARD_BUTTON_TEMPLATE.format(classes='', text='>>')

def compile_function(page):
    """Call question compile functions in index order"""
    [
        compile_function() 
        for q in page.questions for compile_function in q.compile_functions
    ]

def validate_function(page):
    """Call question validate functions in index order"""
    [
        validate_function() 
        for q in page.questions for validate_function in q.validate_functions
    ]
    
def submit_function(page):
    """Call question submit functions in index order"""
    [
        submit_function() 
        for q in page.questions for submit_function in q.submit_functions
    ]