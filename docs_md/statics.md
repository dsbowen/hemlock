<script src="https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_HTMLorMML" type="text/javascript"></script>

<link rel="stylesheet" href="https://assets.readthedocs.org/static/css/readthedocs-doc-embed.css" type="text/css" />

<style>
    a.src-href {
        float: right;
    }
    p.attr {
        margin-top: 0.5em;
        margin-left: 1em;
    }
    p.func-header {
        background-color: gainsboro;
        border-radius: 0.1em;
        padding: 0.5em;
        padding-left: 1em;
    }
    table.field-table {
        border-radius: 0.1em
    }
</style># Statics

Tool for generating statics (embedded images and videos).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**external_css**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>external_css</b>(<i>**attrs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L21">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>**attrs : <i></i></b>
<p class="attr">
    Attribute names and values in the <code>&lt;link/&gt;</code> tag.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>css : <i>str</i></b>
<p class="attr">
    <code>&lt;link/&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>

####Examples

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

##hemlock.tools.**internal_css**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>internal_css</b>(<i>style</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L79">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>style : <i>dict</i></b>
<p class="attr">
    Maps css selector to an attributes dictionary. The attributes dictionary maps attribute names to values.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>css : <i>str</i></b>
<p class="attr">
    <code>&lt;style&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>

####Examples

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
    body {background:coral;}
</style>
```

##hemlock.tools.**external_js**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>external_js</b>(<i>**attrs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L120">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>**attrs : <i></i></b>
<p class="attr">
    Attribute names and values in the <code>&lt;script&gt;</code> tag.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>js : <i>str</i></b>
<p class="attr">
    <code>&lt;script&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>

####Examples

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

##hemlock.tools.**internal_js**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>internal_js</b>(<i>js</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L153">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>js : <i>str</i></b>
<p class="attr">
    Javascript code.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>js : <i>str</i></b>
<p class="attr">
    Javascript code wrapped in <code>&lt;script&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, push_app_context
from hemlock.tools import internal_js

app = push_app_context()

p = Page(
    extra_js=internal_js(
        '''
        $( document ).ready(function() {
            alert('hello, world!');
        });
        '''
    )
)
p.js
```

Out:

```
...
<script>
    $( document ).ready(function() {
        alert('hello, world!');
    });
</script>
```

##hemlock.tools.**src_from_bucket**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>src_from_bucket</b>(<i>filename</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L200">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>filename : <i>str</i></b>
<p class="attr">
    Name of the file in the Google bucket.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>src : <i>str</i></b>
<p class="attr">
    <code>src</code> html attribute which references the specified file in the Google bucket.
</p></td>
</tr>
    </tbody>
</table>

####Examples

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
    src=src_from_bucket('wanna_see_the_code.png'),
    align='center'
).render()
Page(Label(img)).preview()
```

##hemlock.tools.**url_from_bucket**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>url_from_bucket</b>(<i>filename, expiration=1800, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L246">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>filename : <i>str</i></b>
<p class="attr">
    Name of the file in the Google bucket.
</p>
<b>expiration : <i>float, default=1800</i></b>
<p class="attr">
    Number of seconds until the url expires.
</p>
<b>**kwargs : <i></i></b>
<p class="attr">
    Keyword arguments are passed to the [<code>generate_signed_url</code> method] (https://cloud.google.com/storage/docs/access-control/signed-urls).
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>signed_url : <i>str</i></b>
<p class="attr">
    Signed url for the file in the app's bucket.
</p></td>
</tr>
    </tbody>
</table>

####Examples

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
    filename = 'wanna_see_the_code.png'
    url = url_from_bucket(filename)
    return Branch(Page(Download(downloads=[(url, filename)])))
```

In `app.py`:

```python
import survey

from hemlock import create_app

app = create_app()

if __name__ == '__main__':
    from hemlock.app import socketio
    socketio.run(app, debug=True)
```

Run the app locally with:

```
$ python app.py # or python3 app.py
```

And open your browser to <http://localhost:5000/>. Click on the
download button to download the file from your Google bucket.

##hemlock.tools.**Static**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Static</b>(<i>template, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L322">[source]</a>
</p>

Base for static objects (images and videos).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>template : <i>str</i></b>
<p class="attr">
    Path to template file. This is <em>not</em> a Jinja template, as you may wish to generate html for statics outside the application context.
</p>
<b>**kwargs : <i></i></b>
<p class="attr">
    Any attribute of the static object can be set by passing it as a keyword argument.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>body : <i>sqlalchemy_mutablesoup.MutableSoup</i></b>
<p class="attr">
    Html of the static object.
</p>
<b>src_params : <i>dict</i></b>
<p class="attr">
    Maps url parameter names to values. These will be attached to the <code>src</code> html attribute when the static is rendered.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>render</b>(<i>self, tag_selector=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L350">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>tag_selector : <i>str</i></b>
<p class="attr">
    CSS selector for the html tag containing the <code>src</code> attribute.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>html : <i>str</i></b>
<p class="attr">
    Rendered html.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**Img**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Img</b>(<i>template=os.path.join(DIR, 'img.html'), **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L387">[source]</a>
</p>

Static image.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>template : <i>str, default='directory/img.html'</i></b>
<p class="attr">
    Image template. By default, this is a file stored in the directory of the current file.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>align : <i>str</i></b>
<p class="attr">
    Image alignment; <code>'left'</code>, <code>'center'</code>, or <code>'right</code>'.
</p>
<b>caption : <i>str</i></b>
<p class="attr">
    Image caption.
</p>
<b>figure : <i>bs4.Tag</i></b>
<p class="attr">
    <code>&lt;figure&gt;</code> tag.
</p>
<b>img : <i>bs4.Tag</i></b>
<p class="attr">
    <code>&lt;img&gt;</code> tag.
</p>
<b>src : <i>str</i></b>
<p class="attr">
    <code>src</code> attribute of the <code>&lt;img&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, Label, push_app_context
from hemlock.tools import Img

app = push_app_context()

img = Img(
    src='https://imgs.xkcd.com/comics/wanna_see_the_code.png',
    align='center'
).render()
Page(Label(img)).preview()
```

####Methods



<p class="func-header">
    <i></i> <b>render</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L476">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>html : <i>str</i></b>
<p class="attr">
    Rendered image html.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**Vid**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Vid</b>(<i>template=os.path.join(DIR, 'vid.html'), **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L493">[source]</a>
</p>

Static video.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>template : <i>str, default='directory/vid.html'</i></b>
<p class="attr">
    Video template. By default, this is a file stored in the directory of the current file.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>iframe : <i>bs4.Tag</i></b>
<p class="attr">
    <code>&lt;iframe&gt;</code> tag.
</p>
<b>src : <i>str</i></b>
<p class="attr">
    <code>src</code> attribute of the <code>&lt;iframe&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, Label, push_app_context
from hemlock.tools import Vid

app = push_app_context()

vid = Vid.from_youtube('https://www.youtube.com/watch?v=UbQgXeY_zi4')
Page(Label(vid.render())).preview()
```

####Methods



<p class="func-header">
    <i></i> <b>from_youtube</b>(<i>src</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L538">[source]</a>
</p>

Capture the YouTube video id and create an embedded src.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>src : <i>str</i></b>
<p class="attr">
    Link to the YouTube video.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>vid : <i>hemlock.tools.Vid</i></b>
<p class="attr">
    Video object.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>render</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L562">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>html : <i>str</i></b>
<p class="attr">
    Rendered video html.
</p></td>
</tr>
    </tbody>
</table>

