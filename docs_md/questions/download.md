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
</style># Download button

See <https://dsbowen.github.io/flask-download-btn/> for more details.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Download**

<p class="func-header">
    <i>class</i> hemlock.<b>Download</b>(<i>label=None, template='hemlock/download.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/download.py#L13">[source]</a>
</p>

Allows participants to download files.

Inherits from
[`flask_download_btn.DownloadBtnMixin`](https://dsbowen.github.io/flask-download-btn/download_btn_mixin/) and
[`hemlock.Question`](../models/question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Download button label.
</p>
<b>template : <i>str, default='hemlock/download.html'</i></b>
<p class="attr">
    Download button body template.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Download, Page, push_app_context

app = push_app_context()

Page(Download(
    'Click here to download a file.',
    downloads=('HELLO_WORLD_URL', 'hello_world.txt')
)).preview()
```

Replace `'HELLO_WORLD_URL'` with your file download URL. Note that the
download button will not download your file from a preview.

