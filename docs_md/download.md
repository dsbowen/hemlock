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
    <i>class</i> hemlock.<b>Download</b>(<i>label='', template='hemlock/download.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/download.py#L16">[source]</a>
</p>

Allows participants to download files.

Inherits from
[`flask_download_btn.DownloadBtnMixin`](https://dsbowen.github.io/flask-download-btn/download_btn_mixin/) and
[`hemlock.Question`](question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or bs4.BeautifulSoup, default=''</i></b>
<p class="attr">
    Download button label.
</p>
<b>template : <i>str, default='hemlock/download.html'</i></b>
<p class="attr">
    Download button body template.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>create_file_functions : <i>list of hemlock.CreateFile</i></b>
<p class="attr">
    Functions for creating files and executing other operations after form handling and before beginning download. More on [file creation] (https://dsbowen.github.io/flask-download-btn/create/).
</p>
<b>handle_form_functions : <i>list of hemlock.HandleForm</i></b>
<p class="attr">
    Functions for making the download button responsive to web forms. These functions are executed before file creation functions. More on <a href="https://dsbowen.github.io/flask-download-btn/form/">form handling</a>.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Download, Page, push_app_context

app = push_app_context()

Page(Download(
    '<p>Click here to download a file.</p>',
    downloads=[('HELLO_WORLD_URL', 'hello_world.txt')]
)).preview()
```

Replace `'HELLO_WORLD_URL'` with your file download URL. Note that the
download button will not download your file from a preview.



##hemlock.**CreateFile**



Function models for creating files and executing other operations after
form handling and before download.

Inherits from [`hemlock.models.FunctionRegistrar`](functions.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





##hemlock.**HandleForm**



Function models for form handling.

Inherits from [`hemlock.models.FunctionRegistrar`](functions.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



