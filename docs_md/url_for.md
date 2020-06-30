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
</style># url_for

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**url_for**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>url_for</b>(<i>*args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/url_for.py#L5">[source]</a>
</p>

Attempt to return `flask.url_for(*args, **kwargs)`. However, this method
does not exit the program when getting a url outside a request context;
e.g. when debugging in a shell or notebook.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>*args, **kwargs : <i></i></b>
<p class="attr">
    Arguments and keyword arguments will be passed to <code>flask.url_for</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>url : <i>str</i></b>
<p class="attr">
    Output of <code>flask.url_for</code> if possible; otherwise <code>'URL_UNAVAILABLE'</code>.
</p></td>
</tr>
    </tbody>
</table>

