"""# Statics

Tool for generating statics (embedded images and videos).
"""

from sqlalchemy_mutablesoup import SoupBase

from flask import current_app

import re
import os
from datetime import timedelta
from urllib.parse import parse_qs, urlparse, urlencode

DIR = os.path.dirname(os.path.realpath(__file__))
NO_BUCKET_ERR_MSG = """
Enable a Google Cloud Bucket to access this feature.
\n  See `hlk gcloud-bucket`
"""
SRC_ROOT = 'https://storage.googleapis.com'

def src_from_bucket(filename):
    """
    Parameters
    ----------
    filename : str
        Name of the file in the Google bucket.

    Returns
    -------
    src : str
        `src` html attribute which references the specified file in the Google
        bucket.

    Notes
    -----
    You must have a Google bucket associated with this app to use this 
    feature.
    """
    bucket = os.environ.get('BUCKET')
    assert bucket is not None, NO_BUCKET_ERR_MSG
    return '/'.join([SRC_ROOT, bucket, filename])

def url_from_bucket(filename, expiration=3600, **kwargs):
    """
    Parameters
    ----------
    filename : str
        Name of the file in the Google bucket.

    expiration : float, default=3600
        Number of seconds until the url expires.

    \*\*kwargs :
        Keyword arguments are passed to the [`generate_signed_url` method]
        (https://cloud.google.com/storage/docs/access-control/signed-urls).

    Returns
    -------
    signed_url : str
        Signed url for the file in the app's bucket.
    """
    assert hasattr(current_app, 'gcp_bucket'), NO_BUCKET_ERR_MSG
    kwargs['expiration'] = timedelta(expiration)
    blob = current_app.gcp_bucket.blob(filename)
    return blob.generate_signed_url(**kwargs)


class Static():
    """
    Base for static objects (images and videos).

    Parameters
    ----------
    template : str
        Path to template file. This is *not* a Jinja template, as you may 
        wish to generate html for statics outside the application context.

    \*\*kwargs :
        Any attribute of the static object can be set by passing it as a 
        keyword argument.

    Attributes
    ----------
    body : sqlalchemy_mutablesoup.MutableSoup
        Html of the static object.

    src_params : dict
        Maps url parameter names to values. These will be attached to the 
        `src` html attribute when the static is rendered.
    """
    def __init__(self, template, **kwargs):
        self.body = SoupBase(open(template).read(), 'html.parser')
        self.src_params = {}
        [setattr(self, key, val) for key, val in kwargs.items()]

    def render(self, tag_selector=None):
        """
        Parameters
        ----------
        tag_selector : str
            CSS selector for the html tag containing the `src` attribute.

        Returns
        -------
        html : str
            Rendered html.
        """
        body = self.body.copy()
        if tag_selector is not None:
            tag = body.select_one(tag_selector)
            if self.src_params:
                tag['src'] = tag.get('src')+'?'+urlencode(self.src_params)
        return str(body)

    def _set_src(self, tag, src):
        """
        Set the `src` attribute.

        Parameters
        ----------
        tag : bs4.Tag
            Tag containing the `src` attribute.

        src : str
            New value of the `src` attribute.
        """
        # store src params for later; add back when rendering
        self.src_params = parse_qs(urlparse(src).query)
        # set the src as just the url root
        tag['src'] = src.split('?')[0]


class Img(Static):
    """
    Static image.

    Parameters
    ----------
    template : str, default='directory/img.html'
        Image template. By default, this is a file stored in the directory of 
        the current file.

    Attributes
    ----------
    align : str
        Image alignment; `'left'`, `'center'`, or `'right`'.

    caption : str
        Image caption.

    figure : bs4.Tag
        `<figure>` tag.

    img : bs4.Tag
        `<img>` tag.

    src : str
        `src` attribute of the `<img>` tag.

    Examples
    --------
    ```python
    from hemlock import Page, Label, push_app_context
    from hemlock.tools import Img

    push_app_context()
        
    p = Page()
    img = Img(
    \    src='https://imgs.xkcd.com/comics/wanna_see_the_code.png', 
    \    align='center'
    )
    Label(p, label=img.render())

    p.preview() # p.preview('Ubuntu') if working in Ubuntu/WSL
    ```
    """
    def __init__(self, template=os.path.join(DIR, 'img.html'), **kwargs):
        super().__init__(template, **kwargs)

    @property
    def align(self):
        for class_ in self.figure['class']:
            if class_ == 'text-left':
                return 'left'
            if class_ == 'text-center':
                return 'center'
            if class_ == 'text-right':
                return 'right'

    @align.setter
    def align(self, align_):
        align_classes = ['text-'+i for i in ['left','center','right']]
        self.figure['class'] = [
            c for c in self.figure['class'] if c not in align_classes
        ]
        if align_:
            align_ = 'text-' + align_
            self.figure['class'].append(align_)

    @property
    def caption(self):
        return self.body.text('figcaption')

    @caption.setter
    def caption(self, val):
        self.body.set_element('figcaption', val)

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

    def render(self):
        """
        Returns
        -------
        html : str
            Rendered image html.
        """
        return super().render('img')


YOUTUBE_ATTRS = {
    'frameborder': 0,
    'allow': 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture',
    'allowfullscreen': None
}


class Vid(Static):
    """
    Static video.
    
    Parameters
    ----------
    template : str, default='directory/vid.html'
        Video template. By default, this is a file stored in the directory of 
        the current file.

    Attributes
    ----------
    iframe : bs4.Tag
        `<iframe>` tag.

    src : str
        `src` attribute of the `<iframe>` tag.

    Examples
    --------
    ```python
    from hemlock import Page, Label, push_app_context
    from hemlock.tools import Vid

    push_app_context()
        
    p = Page()
    vid = Vid.from_youtube('https://www.youtube.com/watch?v=UbQgXeY_zi4')
    Label(p, label=vid.render())

    p.preview() # p.preview('Ubuntu') if working in Ubuntu/WSL
    ```
    """
    def __init__(self, template=os.path.join(DIR, 'vid.html'), **kwargs):
        super().__init__(template, **kwargs)

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
        """
        Capture the YouTube video id and create an embedded src.
        
        Parameters
        ----------
        src : str
            Link to the YouTube video.

        Returns
        -------
        vid : hemlock.tools.Vid
            Video object.
        """
        vid = Vid()
        params = parse_qs(urlparse(src).query)
        # video id
        id = params.pop('v')[0]
        # src for the embedded video
        vid.src = 'https://www.youtube.com/embed/' + id
        vid.iframe.attrs.update(YOUTUBE_ATTRS)
        vid.params = params
        return vid
        
    def render(self):
        """
        Returns
        -------
        html : str
            Rendered video html.
        """
        return super().render('iframe')