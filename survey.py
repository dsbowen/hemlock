##############################################################################
# Hemlock survey template
# by Dillon Bowen
# last modified 07/24/2019
##############################################################################

# TODO FOR WKHTML
# Local files: use static url_for in survey, convert to abspath for wkhtmltopdf
# URL: use regular src in survey, convert to base64 for wkhtmltopdf 

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
    
    attrs = {'width': 'auto', 'height': 'auto'}
    
    p = Page(b)
    img = image(
        src='wanna_see_the_code.png', classes=['fit', 'center'], 
        attrs=attrs)
    q = Question(p, img)
    
    p = Page(b)
    url = "https://imgs.xkcd.com/comics/wanna_see_the_code_2x.png"
    img = image(
        src=url, src_type='url', classes=['fit', 'center'], 
        attrs=attrs, copy_for_viewing=True)
    q = Question(p, img)
    
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
