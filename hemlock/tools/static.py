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
# filename: name of file in static folder
# format: list of format classes
#   see page.html for format classes
def image(filename, format=[], width='auto', height='auto'):
    return '''
        <img class='{1}' src={0} width='{2}' height='{3}' alt='{0}'
        '''.format(static(filename), ' '.join(format), width, height)