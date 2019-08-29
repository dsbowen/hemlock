##############################################################################
# Static (functions for inserting statics)
# by Dillon Bowen
# last modified 08/29/2019
##############################################################################

import os
from flask import url_for

IMAGE = '''
<img class="{imgclass}" src="{src}" width="{width}" height="{height}" alt="{alt}"/>
'''

# Return html for image
# filename: name of file in static folder
# url: image url
# imgclass: format classes from css
# alt: alt text
def image(
        filename=None, url=None, imgclass='', 
        width='auto', height='auto', alt=None):
    if filename is None and url is None:
        raise ValueError('filename or url required')
    if not (filename is None or url is None):
        raise ValueError('cannot input both filename and url')
    
    src = url if url is not None else url_for('static', filename=filename)
    alt = alt if alt is not None else src
    return IMAGE.format(
        imgclass=imgclass, src=src, width=width, height=height, alt=alt)


