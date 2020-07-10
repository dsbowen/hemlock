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

    Examples
    --------
    Set up a 
    [Google bucket](https://cloud.google.com/storage/docs/creating-buckets)
    with the appropriate 
    [CORS permissions](https://cloud.google.com/storage/docs/cross-origin).

    Set an environment variable `BUCKET` to the name of the bucket.

    ```
    $ export BUCKET=<my-bucket>
    ```

    Upload a file to the bucket, e.g. <https://xkcd.com/2138/> and name it 
    `wanna_see_the_code.png`.

    ```python
    from hemlock import Branch, Page, Label, push_app_context
    from hemlock.tools import Img, src_from_bucket

    app = push_app_context()

    img = Img(
    \    src=src_from_bucket('wanna_see_the_code.png'),
    \    align='center'
    ).render()
    Page(Label(img)).preview()
    ```
    """
    bucket = os.environ.get('BUCKET')
    assert bucket is not None, NO_BUCKET_ERR_MSG
    return '/'.join(['https://storage.cloud.google.com', bucket, filename])

def url_from_bucket(filename, expiration=1800, **kwargs):
    """
    Parameters
    ----------
    filename : str
        Name of the file in the Google bucket.

    expiration : float, default=1800
        Number of seconds until the url expires.

    \*\*kwargs :
        Keyword arguments are passed to the [`generate_signed_url` method]
        (https://cloud.google.com/storage/docs/access-control/signed-urls).

    Returns
    -------
    signed_url : str
        Signed url for the file in the app's bucket.

    Examples
    --------
    Set up a 
    [Google bucket](https://cloud.google.com/storage/docs/creating-buckets)
    with the appropriate 
    [CORS permissions](https://cloud.google.com/storage/docs/cross-origin).

    Set an environment variable `BUCKET` to the name of the bucket, and 
    `GOOGLE_APPLICATION_CREDENTIALS` to the name of your 
    [Google application credentials JSON file](https://cloud.google.com/docs/authentication/getting-started).

    ```
    $ export BUCKET=<my-bucket> GOOGLE_APPLICATION_CREDENTIALS=<my-credentials.json>
    ```

    In `survey.py`:

    ```python
    from hemlock import Branch, Page, Download, route
    from hemlock.tools import url_from_bucket

    @route('/survey')
    def start():
    \    filename = 'wanna_see_the_code.png'
    \    url = url_from_bucket(filename)
    \    return Branch(Page(Download(downloads=[(url, filename)])))
    ```
    
    In `app.py`:

    ```python
    import survey

    from hemlock import create_app

    app = create_app()

    if __name__ == '__main__':
    \    from hemlock.app import socketio
    \    socketio.run(app, debug=True)
    ```

    Run the app locally with:

    ```
    $ python app.py # or python3 app.py
    ```

    And open your browser to <http://localhost:5000/>. Click on the 
    download button to download the file from your Google bucket.
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

    app = push_app_context()
        
    img = Img(
    \    src='https://imgs.xkcd.com/comics/wanna_see_the_code.png', 
    \    align='center'
    ).render()
    Page(Label(img)).preview()
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

    app = push_app_context()
        
    vid = Vid.from_youtube('https://www.youtube.com/watch?v=UbQgXeY_zi4')
    Page(Label(vid.render())).preview()
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