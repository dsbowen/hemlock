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
</style># Worker models

A worker may be attached to a branch or page. Each type of worker is responsible for one of its branch's of page's methods, which is expected to a be a long-running function.

When called, the worker sends the method for which it is responsible to a Redis queue. While the Redis queue is processing the method, participants are shown a loading page. When the worker has finished its job, it returns the loaded page to the participant.

All workers inherit from `flask_worker.WorkerMixin`. See <https://dsbowen.github.io.flask-worker/>.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**CompileWorker**

<p class="func-header">
    <i>class</i> hemlock.<b>CompileWorker</b>(<i>page=None, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/workers.py#L19">[source]</a>
</p>

Handles a page's compile method.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None, default=None</i></b>
<p class="attr">
    The page to which the worker belongs.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>func : <i>callable or None</i></b>
<p class="attr">
    The page's <code>_compile</code> method.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Set from the <code>page</code> parameter.
</p></td>
</tr>
    </tbody>
</table>





##hemlock.**ValidateWorker**

<p class="func-header">
    <i>class</i> hemlock.<b>ValidateWorker</b>(<i>page=None, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/workers.py#L50">[source]</a>
</p>

Handles a page's validate method.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None, default=None</i></b>
<p class="attr">
    The page to which the worker belongs.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>func : <i>callable or None</i></b>
<p class="attr">
    The page's <code>_validate</code> method.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Set from the <code>page</code> parameter.
</p></td>
</tr>
    </tbody>
</table>





##hemlock.**SubmitWorker**

<p class="func-header">
    <i>class</i> hemlock.<b>SubmitWorker</b>(<i>page=None, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/workers.py#L81">[source]</a>
</p>

Handles a page's submit method.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None, default=None</i></b>
<p class="attr">
    The page to which the worker belongs.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>func : <i>callable or None</i></b>
<p class="attr">
    The page's <code>_submit</code> method.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Set from the <code>page</code> parameter.
</p></td>
</tr>
    </tbody>
</table>





##hemlock.**NavigateWorker**

<p class="func-header">
    <i>class</i> hemlock.<b>NavigateWorker</b>(<i>parent=None, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/workers.py#L112">[source]</a>
</p>

Handles a branch's or page's navigate method.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>parent : <i>hemlock.Branch, hemlock.Page, or None, default=None</i></b>
<p class="attr">
    The branch or page to which this worker belongs.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>func : <i>callable or None</i></b>
<p class="attr">
    The branch's or page's <code>navigate_function</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>branch : <i>hemlock.Branch or None</i></b>
<p class="attr">
    Set from the <code>parent</code> parameter.
</p>
<b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Set from the <code>page</code> parameter.
</p></td>
</tr>
    </tbody>
</table>

####Notes

The navigate worker expects to be associated with a branch or page but not
both.

