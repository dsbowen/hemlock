##############################################################################
# Static (functions for inserting statics)
# by Dillon Bowen
# last modified 09/02/2019
##############################################################################

import os
import urllib.parse as urlparse
from flask import url_for

# Arguments:
# src: media source (must be youtube url for videos)
# classes: css classes (see default.min.css for formatting classes)
# attrs: tag attributes
# copy_for_viewing: indicates media should be copied for survey_view download
#   set this to True for temporary media

IMAGE = '''
    <img class="{classes}" src="{src}" {attrs} {cfv}/>
'''

VIDEO = '''
    <div class="video-wrapper">
    <iframe vid="{vid}"  src="{src}" class="video {classes}" {attrs} {cfv} allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
    </div>
'''

YOUTUBE_EMBED_URL = '''https://www.youtube.com/embed/{id}?autoplay={autoplay}'''

def image(src, classes=[], attrs={}, copy_for_viewing=False):
    return media('image', src, classes, attrs, copy_for_viewing)

def video(src, classes=[], attrs={}, copy_for_viewing=False, autoplay=False):
    return media('video', src, classes, attrs, copy_for_viewing, autoplay)
    
# Return static html
# convert src
# convert classes for insert to html
# convert attributes
# convert copy_for_viewing
# return tag as string
def media(media_type, src, classes, attrs, copy_for_viewing, autoplay=None):
    if media_type == 'video':
        parsed = urlparse.urlparse(src)
        vid = urlparse.parse_qs(parsed.query)['v'][0]
        autoplay = 1 if autoplay else 0
        src = YOUTUBE_EMBED_URL.format(id=vid, autoplay=autoplay)
    elif not (src.startswith('data') or src.startswith('http')):
        src = url_for('static', filename=src)
    
    classes = [classes] if type(classes) == str else classes
    classes = ' '.join(classes)
    
    attrs = ' '.join([key+'="'+str(val)+'"' for key, val in attrs.items()])
    
    cfv = 'copy_for_viewing' if copy_for_viewing else ''
    
    if media_type == 'image':
        return IMAGE.format(classes=classes, src=src, attrs=attrs, cfv=cfv)
    elif media_type == 'video':
        return VIDEO.format(vid=vid, classes=classes, src=src, attrs=attrs, cfv=cfv)