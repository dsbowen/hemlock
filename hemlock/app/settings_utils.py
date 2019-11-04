"""Miscellaneous default settings texts and functions"""

from hemlock.tools import Static

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

SOCKET_JS = Static(
    cdn='https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js',
    filename='js/socketio-2.2.0.js',
    blueprint='hemlock'
)

PAGE_CSS = [
    Static(
        cdn='https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
        filename='css/bootstrap-4.3.1.min.css',
        blueprint='hemlock'
    ),
    Static(
        filename='css/default.css',
        blueprint='hemlock'
    )
]

PAGE_JS = [
    Static(
        cdn='https://code.jquery.com/jquery-3.3.1.min.js',
        filename='js/jquery-3.3.1.min.js',
        blueprint='hemlock'
    ),
    Static(
        cdn='https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js',
        filename='js/popper-1.14.7.min.js',
        blueprint='hemlock'
    ),
    Static(
        cdn='https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js',
        filename='js/bootstrap-4.3.1.min.js',
        blueprint='hemlock'
    ),
    Static(
        filename='js/default.js',
        blueprint='hemlock'
    )
]

def compile_function(page):
    """Call question compile functions in index order"""
    [q._compile() for q in page.questions]

def validate_function(page):
    """Call question validate functions in index order"""
    [q._validate() for q in page.questions]
    
def submit_function(page):
    """Call question submit functions in index order"""
    [q._submit() for q in page.questions]