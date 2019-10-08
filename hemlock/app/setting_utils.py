"""Miscellaneous default settings texts and functions"""

from flask import Markup

TIME_EXPIRED = """You have exceeded your time limit for this survey."""

RESTART = """
<p>Click << to return to your in progress survey. Click >> to restart the survey.</p>
<p>If you choose to restart the survey, your responses will not be saved.</p>
"""

SCREENOUT = """
<p>Our records indicate that you have already participated in this or similar surveys.</p>
<p>Thank you for your continuing interest in our research.</p>
"""

BACK_BUTTON = Markup("""
<button id="back-button" name="direction" type="submit" class="btn btn-outline-primary" style="float: left;" value="back"> 
    << 
</button>
""")

FORWARD_BUTTON_GENERIC = """
<button id="forward-button" name="direction" type="submit" class="btn btn-outline-primary {classes}" style="float: right;" value="forward">
    {text}
</button>
"""

FORWARD_BUTTON = Markup(FORWARD_BUTTON_GENERIC.format(classes='', text='>>'))

WORKER_CONTENT = Markup("""
<div class="alert alert-success w-100" style="text-align:center;">
    Loading
</div>
""")

def default_compile_function(page):
    """Calls question compile functions in index order"""
    return [
        compile_f() for q in page.questions for compile_f in q.compile_functions
    ]
    
def default_submit_function(page):
    """Calls question post functions in index order"""
    return [
        submit_f() for q in page.questions for submit_f in q.submit_functions
    ]