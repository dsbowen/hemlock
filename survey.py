##############################################################################
# Hemlock survey template
# by Dillon Bowen
# last modified 07/24/2019
##############################################################################

# import hemlock package, configuration class, and texts
from hemlock import *
from custom_compilers import *
from debug import AIParticipant as AIP
from config import Config
from texts import *
from flask_login import current_user

def Start():
    raise NotImplementedError()
        
def Start():
    b = Branch()
    
    p = Page(b)
    q = Question(p, '<p>This image is local</p>')
    img = image(src='wanna_see_the_code.png', classes=['fit', 'center'])
    q = Question(p, img)
    
    p = Page(b)
    q = Question(p, '<p>This image is from a url</p>')
    url = "https://imgs.xkcd.com/comics/wanna_see_the_code_2x.png"
    img = image(src=url, classes=['fit', 'center'], copy_for_viewing=True)
    q = Question(p, img)
    
    for i in range(10):
        p = Page(b)
        q = Question(p, 'Page {}'.format(i+1))
    
    p = Page(b, terminal=True)
    q = Question(p, 'The End')
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
