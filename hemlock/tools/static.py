"""Static database type

Statics can be:
1. Cascading style sheets (CSS)
2. Javascript (JS)
3. Media
    3.1 Images
    3.2 Videos
"""

from copy import deepcopy
from datetime import timedelta
from flask import Markup, current_app, url_for
from sqlalchemy_mutable import Mutable
import os
import urllib.parse as urlparse


class StaticBase(Mutable):
    _external = False

    @property
    def _url(self):
        """Format URL for HTML tag"""
        if not current_app.offline:
            if self.url is not None:
                return self.url
            if self.use_bucket:
                return self.bucket_url()
        if self.filename is not None:
            return self.app_url()
        return ''

    @property
    def _attrs(self):
        """Format attributes for HTML tag"""
        return ' '.join([k+'="'+str(v)+'"' for k, v in self.attrs.items()])

    @property
    def _parms(self):
        """Format paramters for URL"""
        return self._format_parms(self.parms)

    def __init__(
            self, url=None, filename=None, blueprint=None, use_bucket=False,
            attrs={}, parms={}
        ):
        self.url = url
        self.filename = filename
        self.blueprint = blueprint
        self.use_bucket = use_bucket
        self.attrs = attrs
        self.parms = parms

    def app_url(self):
        """Return URL of static stored in application slug"""
        bp = self.blueprint+'.' if self.blueprint is not None else ''
        url = url_for(
            bp+'static', filename=self.filename, _external=self._external
        )
        return self._format_url(url)

    def bucket_url(self):
        """Return URL of static stored in Google bucket"""
        blob = current_app.gcp_bucket.get_blob(self.filename)
        return blob.generate_signed_url(expiration=timedelta(hours=1))

    def local_path(self):
        """Return the path to the local resource"""
        if self.filename is None:
            return ''
        if self.blueprint is None:
            path = current_app.static_folder
        else:
            path = current_app.blueprints[self.blueprint].static_folder
        return os.path.join(path, self.filename)

    def _format_parms(self, parms):
        """Format parameters for URL"""
        return '&'.join([k+'='+str(v) for k, v in parms.items()])

    def _format_url(self, url=None):
        """Format URL with parameters"""
        if not self.parms:
            return url
        return url+'?'+self._parms if url is not None else ''


CSS_TEMPLATE = """
<link href="{static._url}" rel="stylesheet" type="text/css" {static._attrs}/>
"""

class CSS(StaticBase):
    def render(self):
        return CSS_TEMPLATE.format(static=self)


JS_TEMPLATE = """
<script src="{static._url}" {static._attrs}>
</script>
"""

class JS(StaticBase):
    def render(self):
        return JS_TEMPLATE.format(static=self)


class MediaBase(StaticBase):
    # Media require external links for survey viewing
    _external = True

    @property
    def _classes(self):
        """Format classes for HTML tag"""
        return ' '.join(self.classes)

    @property
    def _cfv(self):
        """Format copy for viewing for HTML tag"""
        return 'copy_for_viewing' if self.copy_for_viewing else ''

    def __init__(
            self, classes=[], copy_for_viewing=False, *args, **kwargs
        ):
        self.classes = classes
        self.copy_for_viewing = copy_for_viewing
        super().__init__(*args, **kwargs)


IMG_TEMPLATE = """
<img class="{static._classes}" src="{static._url}" {static._attrs} {static._cfv}/>
"""

class Img(MediaBase):
    def render(self):
        return IMG_TEMPLATE.format(static=self)


VID_TEMPLATE =  """
<div class="video-wrapper">
    <iframe src="{static._url}" class="video {static._classes}" {static._attrs} {static._cfv}>
    </iframe>
</div>
"""

class Vid(MediaBase):
    def render(self):
        return VID_TEMPLATE.format(static=self)


YOUTUBE_DEFAULT_ATTRS = {
    'frameborder': 0,
    'allow': 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture',
    'allowfullscreen': None
}

YOUTUBE_EMBED_URL = 'https://www.youtube.com/embed/{vid}'

class YouTubeVid(Vid):
    @property
    def _url(self):
        """Use YouTube embedded URL as the URL"""
        url = YOUTUBE_EMBED_URL.format(vid=self._get_vid())
        return self._format_url(url)

    @property
    def _parms(self):
        """Update the src paramters with instance parameters"""
        src_parms = self._get_src_parms()
        src_parms.pop('v')
        src_parms.update(self.parms)
        return self._format_parms(src_parms)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.attrs:
            self.attrs = deepcopy(YOUTUBE_DEFAULT_ATTRS)

    def _get_vid(self):
        """Get ID of the YouTube video"""
        return self._get_src_parms()['v']

    def _get_src_parms(self):
        """Get src parameters from video URL"""
        parsed = urlparse.urlparse(self.url)
        src_parms = urlparse.parse_qs(parsed.query)
        src_parms = {k: v[0] for k, v in src_parms.items()}
        return src_parms

    def render(self):
        self.attrs.update({'vid': self._get_vid()})
        return super().render()