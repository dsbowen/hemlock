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
</style>##hemlock.tools.**attention_check**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>attention_check</b>(<i>make_failure_page=_make_failure_page, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/attention.py#L41">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>make_failure_page : <i>callable, default=make_failure_page</i></b>
<p class="attr">
    Returns a terminal page to take participants to after failing the check.
</p>
<b>**kwargs : <i></i></b>
<p class="attr">
    Attributes of the attention check input. Should not include <code>debug</code> or <code>submit</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>check : <i>Input</i></b>
<p class="attr">
    Attention check input.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Page, push_app_context
from hemlock.tools import attention_check

app = push_app_context()

Page(attention_check()).preview()
```