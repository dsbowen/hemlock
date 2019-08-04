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
    name = Question(p, 'What is your name?', var='name', qtype='free')
    Validator(name, require)
    
    p = Page(b)
    ice_cream = Question(
        p, 'Favorite ice cream:', var='ice_cream', qtype='single choice')
    ice_cream.default(Choice(ice_cream, 'Vanilla'))
    Choice(ice_cream, 'Chocolate')
    Choice(ice_cream, 'Strawberry')
    Choice(ice_cream, 'Cookies and cream')
    Choice(ice_cream, 'Mint chocolate chip')
    ice_cream.randomize()
    Validator(ice_cream, require)
    
    b.next(End, {'name_id':name.id, 'ice_cream_id':ice_cream.id})
    
    return b
    
def End(name_id, ice_cream_id):
    name, ice_cream = [q.get_response() 
        for q in query([name_id, ice_cream_id])]
    
    b = Branch()
    p = Page(b, terminal=True)
    q = Question(p, 'Your name is {0} and your favorite ice cream is {1}'.format(name, ice_cream))
    
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
