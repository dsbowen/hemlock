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
    color = Question(
        p, "What's your favorite color?", qtype='single choice', var='Color')
    color.default(Choice(color, 'Pink'))
    Choice(color, 'Blue')
    Choice(color, 'White')
    
    name = Question(
        p, "What's your middle name?", qtype='free', var='MiddleName')
    Validator(name, require)
    
    b.next(End, {'name':name, 'color':color})
    
    return b
    
def End(name, color):
    name = name.get_response()
    color = color.get_response()
    
    b = Branch()
    p = Page(b, terminal=True)
    q = Question(p, 'Nice to meet you, {0}! My favorite color is also {1}'.format(name, color))
    
    return b
    
      
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
