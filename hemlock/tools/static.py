###############################################################################
# Static (function for inserting statics)
# by Dillon Bowen
# last modified 06/04/2019
###############################################################################

from flask import url_for

# Return url path for static file
def static(filename):
    return url_for('static', filename=filename)