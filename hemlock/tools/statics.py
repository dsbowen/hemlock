"""Tool for generating statics (embedded images and videos)"""

from sqlalchemy_mutablesoup import SoupBase

from flask import current_app

from datetime import timedelta
from urllib.parse import parse_qs, urlparse, urlencode
import re
import os

NO_BUCKET_ERR_MSG = '''
Enable a Google Cloud Bucket to access this feature.
\n  See `hlk gcloud-bucket`
'''
SRC_ROOT = 'https://storage.googleapis.com'

def src_from_bucket(filename):
    """Get `src` attribute from Google bucket"""
    bucket_name = os.environ.get('BUCKET')
    assert bucket_name is not None, NO_BUCKET_ERR_MSG
    return '/'.join([SRC_ROOT, bucket_name, filename])

def url_from_bucket(filename, **kwargs):
    """Get url attribute from Google bucket

    By default, the link expires in 3600 seconds.
    """
    assert hasattr(current_app, 'gcp_bucket'), NO_BUCKET_ERR_MSG
    kwargs['expiration'] = kwargs.get('expriation') or timedelta(3600)
    blob = current_app.gcp_bucket.blob(filename)
    return blob.generate_signed_url(**kwargs)


class Static():
    """Static base

    This base stores its HTML in a `MutableSoup` object called `body`. The source parameters are stored separately in a `src_parms` dictionary. These are added to the src attribute when rendering.
    """
    def __init__(self, template, **kwargs):
        path = os.path.dirname(os.path.realpath(__file__))
        html = open(os.path.join(path, template)).read()
        self.body = SoupBase(html, 'html.parser')
        self.src_parms = {}
        [setattr(self, key, val) for key, val in kwargs.items()]

    def render(self, tag_selector=None):
        body = self.body.copy()
        if tag_selector is not None:
            tag = body.select_one(tag_selector)
            if self.parms:
                tag['src'] = tag.get('src')+'?'+urlencode(self.parms)
        return str(body)

    def _set_src(self, tag, url):
        self.parms = parse_qs(urlparse(url).query)
        tag['src'] = url.split('?')[0]


class Img(Static):
    """Image"""
    def __init__(self, **kwargs):
        super().__init__('img.html', **kwargs)

    @property
    def figure(self):
        return self.body.select_one('figure')

    @property
    def img(self):
        return self.body.select_one('img')

    @property
    def src(self):
        return self.img.attrs.get('src')

    @src.setter
    def src(self, val):
        super()._set_src(self.img, val)

    @property
    def caption(self):
        return self.body.text('figcaption')

    @caption.setter
    def caption(self, val):
        self.body.set_element('figcaption', val)

    @property
    def alignment(self):
        for class_ in self.figure['class']:
            if class_ == 'text-left':
                return 'left'
            if class_ == 'text-center':
                return 'center'
            if class_ == 'text-right':
                return 'right'

    @alignment.setter
    def alignment(self, align):
        align_classes = ['text-'+i for i in ['left','center','right']]
        self.figure['class'] = [
            c for c in self.figure['class'] if c not in align_classes
        ]
        if align:
            align = 'text-' + align
            self.figure['class'].append(align)

    def render(self):
        return super().render('img')


YOUTUBE_ATTRS = {
    'frameborder': 0,
    'allow': 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture',
    'allowfullscreen': None
}


class Vid(Static):
    """Video"""
    def __init__(self, **kwargs):
        super().__init__('vid.html', **kwargs)

    @property
    def iframe(self):
        return self.body.select_one('iframe')

    @property
    def src(self):
        return self.iframe.attrs.get('src')

    @src.setter
    def src(self, val):
        super()._set_src(self.iframe, val)

    def from_youtube(src):
        """Capture the YouTube video id and create an embedded src"""
        vid = Vid()
        parms = parse_qs(urlparse(src).query)
        id = parms.pop('v')[0] # video id
        vid.src = 'https://www.youtube.com/embed/' + id
        vid.iframe.attrs.update(YOUTUBE_ATTRS)
        vid.parms = parms
        return vid
        
    def render(self):
        return super().render('iframe')