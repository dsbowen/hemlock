##############################################################################
# Hemlock survey template
# by Dillon Bowen
# last modified 07/24/2019
##############################################################################

# import hemlock package, configuration class, and texts
from hemlock import *
from debug import AIParticipant as AIP
from config import Config
from texts import *
from flask_login import current_user

def Start():
    raise NotImplementedError()
    
def Start():
    b = Branch()
    p = Page(b)
    q = Question(p, 'Please enter your name', qtype='free', var='name')
    Validator(q, require)
    p = Page(b)
    q = Question(
        p, 'What is your favorite flavor of ice cream?', 
        qtype='single choice', var='ice_cream')
    Choice(q, 'Lavender')
    Choice(q, 'Chocolate')
    Choice(q, 'Orange')
    q.randomize()
    Validator(q, require)
    p = Page(b, compile=print_html, terminal=True)
    q = Question(p, 'goodbye world')
    return b

def print_html(p):
    print([i for i in current_user._page_html])
      
# create the application (survey)
app = create_app(
    Config,
    start=Start,
    password='',
    record_incomplete=False,
    block_duplicate_ips=False,
    block_from_csv='block.csv',
    debug=True)
    
# run app
if __name__ == '__main__':
    app.run()
    
# hemlock shell
import hemlock_shell
