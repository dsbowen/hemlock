##############################################################################
# Static (functions for inserting statics)
# by Dillon Bowen
# last modified 08/30/2019
##############################################################################

import os
from flask import url_for

IMAGE = '''
    <img class="{classes}" src="{src}" src_type="{src_type}" {attrs} {copy_for_viewing}/>
'''

# Return html for image
# arguments:
#   src: image source (filename, url, or data)
#   src_type: source type ('local', 'url', or 'data')
#   classes: tag classes (see default.min.css for formatting classes)
#   attrs: tag attributes
#   copy_for_viewing: indicates that image should be copied
#       for survey_view download; set to True for temporary images
# convert src using url_for if local
# convert classes for insert to html
# convert attributes
# convert copy_for_vieweing
# return tag as string
def image(
        src, src_type='local', classes=[], attrs={}, 
        copy_for_viewing=False):
    src = url_for('static', filename=src) if src_type=='local' else src
    
    classes = [classes] if type(classes) == str else classes
    classes = ' '.join(classes)
    
    attrs = ' '.join([key+'="'+str(val)+'"' for key, val in attrs.items()])
    
    copy_for_viewing = 'copy_for_viewing' if copy_for_viewing else ''
    
    return IMAGE.format(
        classes=classes, src=src, src_type=src_type, attrs=attrs, 
        copy_for_viewing=copy_for_viewing)


