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
</style># File upload

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**upload_to_bucket**

<p class="func-header">
    <i>def</i> hemlock.<b>upload_to_bucket</b>(<i>file_</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/file.py#L20">[source]</a>
</p>

Default `hemlock.File` submit function. Uploads a participant file to
Google bucket.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>file_ : <i>hemlock.File</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**File**

<p class="func-header">
    <i>class</i> hemlock.<b>File</b>(<i>page=None, template='hemlock/file.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/file.py#L44">[source]</a>
</p>

Allows participants to upload files.

Inherits from [`hemlock.InputGroup`](input_group.md),
[`hemlock.InputBase`](bases.md), and [`hemlock.Question`](question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None, default=None</i></b>
<p class="attr">
    Page to which this file belongs.
</p>
<b>template : <i>str, default='hemlock/file.html'</i></b>
<p class="attr">
    Template for the file upload body.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>allowed_extensions : <i>list</i></b>
<p class="attr">
    Allowed file extensions, e.g. <code>['.png','.jpeg']</code>.
</p>
<b>filename : <i>str</i></b>
<p class="attr">
    Name of the file as stored in the Google bucket.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, File, push_app_context

push_app_context()

p = Page()
File(p, label='<p>Upload .png file.</p>', allowed_extensions=['.png'])
p.preview() # p.preview('Ubuntu') if working in Ubuntu/WSL
```

####Methods



<p class="func-header">
    <i></i> <b>generate_signed_url</b>(<i>self, expiration=timedelta(hours=0.5), **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/file.py#L89">[source]</a>
</p>

Generate a signed URL for the uploaded file.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>expiration : <i>datetime.timedelta, default=datetime.timedelta(0, 1800)</i></b>
<p class="attr">
    Duration for which this signed URL is valid.
</p>
<b>**kwargs : <i></i></b>
<p class="attr">
    Additional keyword arguments are passed to the <code>generate_signed_url</code> method.
</p></td>
</tr>
    </tbody>
</table>

####Notes

Read more about [signed URLs](https://cloud.google.com/storage/docs/access-control/signed-urls).



<p class="func-header">
    <i></i> <b>get_allowed_types</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/file.py#L112">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>allowed_types : <i>list</i></b>
<p class="attr">
    List of allowed mimetypes. Derived from <code>self.allowed_extensions</code>.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>get_path</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/file.py#L122">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>path : <i>str</i></b>
<p class="attr">
    Path to the uploaded file in the Google bucket.
</p></td>
</tr>
    </tbody>
</table>

