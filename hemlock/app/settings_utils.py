"""Miscellaneous default settings texts and functions"""

from hemlock.tools import CSS, JS

from random import random, shuffle
from time import sleep

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

SOCKET_JS = JS(
    url='https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js',
    filename='js/socketio-2.2.0.js',
    blueprint='hemlock'
)

PAGE_CSS = [
    CSS(
        url='https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css',
        filename='css/bootstrap-4.3.1.min.css',
        blueprint='hemlock'
    ),
    CSS(
        filename='css/default.css',
        blueprint='hemlock'
    )
]

PAGE_JS = [
    JS(
        url='https://code.jquery.com/jquery-3.3.1.min.js',
        filename='js/jquery-3.3.1.min.js',
        blueprint='hemlock'
    ),
    JS(
        url='https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js',
        filename='js/popper-1.14.7.min.js',
        blueprint='hemlock'
    ),
    JS(
        url='https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js',
        filename='js/bootstrap-4.3.1.min.js',
        blueprint='hemlock'
    ),
    JS(
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

def debug_function(page, driver):
    """Call question debug functions in random order then navigate"""
    order = [i for i, q in enumerate(page.questions)]
    shuffle(order)
    [page.questions[i]._debug(driver) for i in order]
    forward_exists = back_exists = True
    if random() < .8:
        try:
            driver.find_element_by_id('forward-button').click()
        except:
            forward_exists = False
    if random() < .5:
        try:
            driver.find_element_by_id('back-button').click()
        except:
            back_exists = False
    if not (forward_exists or back_exists):
        sleep(3)
    driver.refresh()
    

def clean_data(df):
    return df