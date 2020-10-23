"""# Statics

Tool for embedding statics:

- css
- javascript
- images
- iframes
- YouTube videos
- links to Google bucket files
"""

from flask import current_app

import re
import os
from datetime import timedelta
from urllib.parse import parse_qs, urlparse, urlencode

DIR = os.path.dirname(os.path.realpath(__file__))

def format_attrs(**attrs):
    """
    Parameters
    ----------
    \*\*attrs : dict
        Maps HTML attribute name to value.

    Returns
    -------
    attrs : str
        Formated attributes for insertion into HTML tag.
    """
    def format_item(key, val):
        if not val:
            # val is empty string, None, False, etc.
            return ''
        return key if val is True else '{}="{}"'.format(key, val)

    attrs = attrs.copy()
    if 'class' in attrs and isinstance(attrs['class'], list):
        attrs['class'] = ' '.join(attrs['class'])
    if 'style' in attrs and isinstance(attrs['style'], dict):
        attrs['style'] = ' '.join(
            ['{}:{};'.format(*item) for item in attrs['style'].items()
        ])
    return ' '.join(format_item(*item) for item in attrs.items())

def external_css(href, rel='stylesheet', type='text/css', **attrs):
    """
    Parameters
    ----------
    \*\*attrs :
        Attribute names and values in the `<link/>` tag.

    Returns
    -------
    css : str
        `<link/>` tag.

    Examples
    --------
    ```python
    from hemlock import Page, push_app_context
    from hemlock.tools import external_css

    app = push_app_context()

    p = Page(extra_css=external_css(href='https://my-css-url'))
    p.css
    ```

    Out:

    ```
    ...
    <link href="https://my-css-url" rel="stylesheet" type="text/css"/>
    ```
    """
    return '<link {}/>'.format(
        format_attrs(href=href, rel=rel, type=type, **attrs)
    )

def internal_css(style):
    """
    Parameters
    ----------
    style : dict
        Maps css selector to an attributes dictionary. The attributes 
        dictionary maps attribute names to values.

    Returns
    -------
    css : str
        `<style>` tag.

    Examples
    --------
    ```python
    from hemlock import Page, push_app_context
    from hemlock.tools import internal_css

    app = push_app_context()

    p = Page(extra_css=internal_css({'body': {'background': 'coral'}}))
    p.css
    ```

    Out:

    ```
    ...
    <style>
    \    body {background:coral;}
    </style>
    ```
    """
    def format_style(selector, attrs):
        attrs = ' '.join(['{}: {};'.format(*item) for item in attrs.items()])
        return selector+' {'+attrs+'}'

    css = ' '.join([format_style(key, val) for key, val in style.items()])
    return '<style>{}</style>'.format(css)

def external_js(src, **attrs):
    """
    Parameters
    ----------
    src : str
        External javascript source.

    \*\*attrs :
        Attribute names and values in the `<script>` tag.

    Returns
    -------
    js : str
        `<script>` tag.

    Examples
    --------
    ```python
    from hemlock import Page, push_app_context
    from hemlock.tools import external_js

    app = push_app_context()

    p = Page(extra_js=external_js(src='https://my-js-url'))
    p.js
    ```

    Out:

    ```
    ...
    <script src="https://my-js-url"></script>
    ```
    """
    return '<script {}></script>'.format(format_attrs(src=src, **attrs))

def internal_js(js, **attrs):
    """
    Parameters
    ----------
    js : str
        Javascript code.

    \*\*attrs : dict
        Mapping of HTML attributes to values for the `<script>` tag.

    Returns
    -------
    js : str
        Javascript code wrapped in `<script>` tag.

    Examples
    --------
    ```python
    from hemlock import Page, push_app_context
    from hemlock.tools import internal_js

    app = push_app_context()

    p = Page(
    \    extra_js=internal_js(
    \        '''
    \        $( document ).ready(function() {
    \            alert('hello, world!');
    \        });
    \        '''
    \    )
    )
    p.js
    ```

    Out:

    ```
    ...
    <script>
    \    $( document ).ready(function() {
    \        alert('hello, world!');
    \    });
    </script>
    ```
    """
    if not js.startswith('<script>'):
        js = '<script {}>{}</script>'.format(format_attrs(**attrs), js)
    return js

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

def img(
    src, caption='', img_align='left', caption_align='left',
    figure_class='figure w-100', figure_attrs={},
    img_class='figure-img img-fluid rounded', img_attrs={},
    caption_class='figure-caption', caption_attrs={},
    template=os.path.join(DIR, 'img.html')
):
    """
    Parameters
    ----------
    src : str
        Image source.

    caption : str

    img_align : str, default='left'

    caption_align : str, default='left'

    figure_class : list or str, default='figure w-100'
        Class for the `<figure>` tag.

    figure_attrs : dict, default={}
        HTML attributes for the `<figure>` tag.

    img_class : list or str, default='figure-img img-fluid rounded'
        Class for the `<img>` tag.

    img_attrs : dict, default={}
        HTML attributes for the `<img>` tag.

    caption_class : list or str, default='figure-caption'
        Class for the `<figcaption>` tag.

    caption_attrs : dict, default={}
        HTML attributes for the `<figcaption>` tag.

    template : str, default='directory/img.html'
        Path to image template. Default is a template in the same directory as
        the current file. This may also be a string to be used directly as the
        template.

    Returns
    -------
    img : str
        Image html.

    Examples
    --------
    ```python
    from hemlock.tools import img

    img(
    \    'https://imgs.xkcd.com/comics/wanna_see_the_code.png',
    \    img_align='center', caption='Wanna See The Code?'
    )
    ```

    Out:

    ```
    <figure class="figure w-100 text-center">
    \    <img class="figure-img img-fluid rounded" src="https://imgs.xkcd.com/comics/wanna_see_the_code.png">
    \    <figcaption class="figure-caption text-left">Wanna See The Code?</figcaption>
    </figure>
    ```
    """
    _add_class(figure_attrs, figure_class)
    figure_attrs['class'].append('text-'+img_align)
    _add_class(img_attrs, img_class)
    img_attrs['src'] = src
    _add_class(caption_attrs, caption_class)
    caption_attrs['class'].append('text-'+caption_align)
    if os.path.exists(template):
        template = open(template).read()
    return template.format(
        figure_attrs=format_attrs(**figure_attrs),
        img_attrs=format_attrs(**img_attrs),
        caption_attrs=format_attrs(**caption_attrs),
        caption=caption
    )

def iframe(
    src, aspect_ratio=(16, 9), query_string={},
    div_class='embed-responsive', div_attrs={},
    iframe_class='embed-responsive-item', 
    iframe_attrs={'allowfullscreen': True},
    template=os.path.join(DIR, 'iframe.html')
):
    """
    Parameters
    ----------
    src : str
        Embed source.

    aspect_ratio : tuple of (int, int), default=(16, 9)
        Embed 
        [aspect ratio](https://getbootstrap.com/docs/4.0/utilities/embed/#aspect-ratios).

    query_string : dict
        Mapping of URL query keys to values.

    div_class : str or list, default='embed-responsive'
        Class of the `<div>` which wraps the `<iframe>`.

    div_attrs : dict, default={}
        HTML attributes for the `<div>` wrapper.

    iframe_class : str or list, default='embed-responsive-item'
        Class of the `<iframe>` tag.

    iframe_attrs : dict, default={'allowfullscreen': True}
        HTML attributes for the `<iframe>` tag.

    template : str, default='directory/iframe.html'
        Path to iframe template. Default is a template in the same directory 
        as the current file. This may also be a string to be used directly as 
        the template.

    Returns
    -------
    iframe : str
        Iframe HTML.

    Examples
    --------
    ```python
    from hemlock.tools import iframe

    iframe(
    \    'https://www.youtube.com/embed/zpOULjyy-n8?rel=0', 
    \    aspect_ratio=(21, 9)
    )
    ```

    Out:

    ```
    <div class="embed-responsive embed-responsive-21by9">
    \    <iframe allowfullscreen class="embed-responsive-item" src="https://www.youtube.com/embed/zpOULjyy-n8?rel=0"></iframe>
    </div>
    ```
    """
    _add_class(div_attrs, div_class)
    div_attrs['class'].append('embed-responsive-{}by{}'.format(*aspect_ratio))
    _add_class(iframe_attrs, iframe_class)
    if query_string:
        src += '?' + urlencode(query_string)
    iframe_attrs['src'] = src
    if os.path.exists(template):
        template = open(template).read()
    return template.format(
        div_attrs=format_attrs(**div_attrs),
        iframe_attrs=format_attrs(**iframe_attrs)
    )

def youtube(
    src, iframe_attrs={
        'allow': 'accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture;', 
        'allowfullscreen': True
    }, *args, **kwargs
):
    """
    Embed a youtube video.

    Parameters
    ----------
    src : str
        Link to youtube video. e.g. 
        <https://www.youtube.com/watch?v=ts3s738ZkcQ>.

    iframe_attrs : dict
        HTML attributes for the `<iframe>` tag.

    \*args, \*\*kwarg : 
        Arguments and keyword arguments are passed to `hemlock.tools.iframe`.

    Returns
    -------
    iframe : str
        Iframe HTML.

    Examples
    --------
    ```python
    from hemlock.tools import youtube

    youtube(
    \    'https://www.youtube.com/watch?v=ts3s738ZkcQ', 
    \    query_string={'autoplay': 1}
    )
    ```

    Out:

    ```
    <div class="embed-responsive embed-responsive-16by9">
    \    <iframe allow="accelerometer; autoplay; encrypted-media; gyroscope; picture-in-picture;" allowfullscreen class="embed-responsive-item" src="https://www.youtube.com/embed/ts3s738ZkcQ?autoplay=1"></iframe>
    </div>
    ```
    """
    video_id = parse_qs(urlparse(src).query).pop('v')[0]
    src = 'https://www.youtube.com/embed/{}'.format(video_id)
    return iframe(src, *args, iframe_attrs=iframe_attrs, **kwargs)

def _add_class(attrs, class_):
    attrs['class'] = class_ if isinstance(class_, list) else [class_]