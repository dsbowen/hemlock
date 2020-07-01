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



##hemlock.tools.**src_from_bucket**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>src_from_bucket</b>(<i>filename</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L22">[source]</a>
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

####Notes

You must have a Google bucket associated with this app to use this
feature.

##hemlock.tools.**url_from_bucket**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>url_from_bucket</b>(<i>filename, expiration=3600, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L44">[source]</a>
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
<b>expiration : <i>float, default=3600</i></b>
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



##hemlock.tools.**Static**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Static</b>(<i>template, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L69">[source]</a>
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
    Path to template file.
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

####Notes

The `template` parameter is *not* a Jinja template, as programmers may wish to generate html for statics outside the application context.

####Methods



<p class="func-header">
    <i></i> <b>render</b>(<i>self, tag_selector=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L100">[source]</a>
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
    <i>class</i> hemlock.tools.<b>Img</b>(<i>template=os.path.join(DIR, 'img.html'), **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L137">[source]</a>
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

push_app_context()

p = Page()
img = Img(
    src='https://imgs.xkcd.com/comics/wanna_see_the_code.png',
    align='center'
)
Label(p, label=img.render())

p.preview() # p.preview('Ubuntu') if working in Ubuntu/WSL
```

####Methods



<p class="func-header">
    <i></i> <b>render</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L229">[source]</a>
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
    <i>class</i> hemlock.tools.<b>Vid</b>(<i>template=os.path.join(DIR, 'vid.html'), **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L246">[source]</a>
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

push_app_context()

p = Page()
vid = Vid.from_youtube('https://www.youtube.com/watch?v=UbQgXeY_zi4')
Label(p, label=vid.render())

p.preview() # p.preview('Ubuntu') if working in Ubuntu/WSL
```

####Methods



<p class="func-header">
    <i></i> <b>from_youtube</b>(<i>src</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L294">[source]</a>
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
    <i></i> <b>render</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/statics.py#L318">[source]</a>
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

