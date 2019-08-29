###############################################################################
# Static (functions for inserting statics)
# by Dillon Bowen
# last modified 06/04/2019
###############################################################################

import os
from flask import url_for

# Return url path for static file
def static(filename):
    print(os.getcwd())
    print(url_for('static', filename=filename))
    path = os.path.join(os.getcwd(), url_for('static', filename=filename)[1:])
    path = path.replace('\\', '/')
    return path
    
# Return html for image
# filename: name of file in static folder
# format: list of format classes
#   see /static/css/default.min.css for format classes
def image(filename, format=[], width='auto', height='auto'):
    return '''
        <img class='{1}' src={0} width='{2}' height='{3}' alt='{0}'>
        '''.format(static(filename), ' '.join(format), width, height)