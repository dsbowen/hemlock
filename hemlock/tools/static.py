###############################################################################
# Static (functions for inserting statics)
# by Dillon Bowen
# last modified 06/04/2019
###############################################################################

from flask import url_for

# Return url path for static file
def static(filename):
    return url_for('static', filename=filename)
    
# Return html for image
def image(filename):
    return '''
        <img class='center-fit' src={0} alt='{0}'
        '''.format(static(filename))