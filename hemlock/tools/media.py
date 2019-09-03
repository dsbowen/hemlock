##############################################################################
# Static (functions for inserting statics)
# by Dillon Bowen
# last modified 09/02/2019
##############################################################################

import os
import urllib.parse as urlparse
from flask import url_for
from copy import deepcopy

# Image tag
IMAGE = '''
    <img class="{classes}" src="{src}" {attrs} {cfv}/>
'''

# Video tag
VIDEO = '''
    <div class="video-wrapper">
    <iframe vid="{vid}"  src="{src}" class="video {classes}" {attrs} {cfv}>
    </iframe>
    </div>
'''

# URL for embedding YouTube video
YOUTUBE_EMBED_URL = '''https://www.youtube.com/embed/{id}?{parms}'''

# Default attributes for video tag
VIDEO_DEFAULT_ATTRS = {
    'frameborder': 0,
    'allow': 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture',
    'allowfullscreen': None
    }

# Return html for image tag
# src: image source (local filename, url, or uri)
# classes: css classes (see default.min.css for formatting classes)
# attrs: tag attributes
# copy_for_viewing: indicates image should be copied for survey_view download
#   set this to True for temporary media
# convert source to local path if image is local
# return tag
def image(src, classes=[], attrs={}, copy_for_viewing=False):
    if not (src.startswith('data') or src.startswith('http')):
        src = url_for('static', filename=src)
    classes, attrs, cfv = media(classes, attrs, copy_for_viewing)
    return IMAGE.format(classes=classes, src=src, attrs=attrs, cfv=cfv)

# Return html for video tag
# parms: youtube video url parameters
# get video id
# add youtube url parms to parms dict unless already in parms
# convert parms and src to html format
# return tag
def video(src, classes=[], attrs={}, copy_for_viewing=False, parms={}):
    vid, parms = get_parms(src, parms)
    src = YOUTUBE_EMBED_URL.format(id=vid, parms=parms)
    video_attrs = deepcopy(VIDEO_DEFAULT_ATTRS)
    video_attrs.update(attrs)
    classes, attrs, cfv = media(classes, video_attrs, copy_for_viewing)
    return VIDEO.format(
        vid=vid, classes=classes, src=src, attrs=attrs, cfv=cfv)

# Get video id and url parameters
def get_parms(src, parms):
    parsed = urlparse.urlparse(src)
    src_parms = urlparse.parse_qs(parsed.query)
    src_parms = {k: v[0] for k, v in src_parms.items()}
    vid = src_parms['v']
    del src_parms['v']
    src_parms.update(parms)
    src_parms = '&'.join([k+'='+str(v) for k,v in src_parms.items()])
    return vid, src_parms
    
# Return html attributes for media
# convert classes to html format
# convert attributes
# convert copy_for_viewing
# return tuple (classes, attributes, copy_for_viewing)
def media(classes, attrs, copy_for_viewing):
    classes = [classes] if type(classes) == str else classes
    classes = ' '.join(classes)
    attrs = ' '.join([key+'="'+str(val)+'"' for key, val in attrs.items()])
    copy_for_viewing = 'copy_for_viewing' if copy_for_viewing else ''
    return (classes, attrs, copy_for_viewing)