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

A worker may be attached to a branch or page. Each type of worker is
responsible for one of its branch's of page's methods, which is expected to
a be a long-running function.

When called, the worker sends the method for which it is responsible to a
Redis queue. While the Redis queue is processing the method, participants
are shown a loading page. When the worker has finished its job, it returns
the loaded page to the participant.

All workers inherit from
[`flask_worker.WorkerMixin`](https://dsbowen.github.io.flask-worker/)..

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Worker**



Convenience methods for adding workers to branches and pages.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

####Examples

We have two files in our root directory. In `survey.py`:

```python
from hemlock import Branch, Page, Label, Navigate, Worker, route

@route('/survey')
def start():
    return Worker.navigate(Navigate.end(Branch(
        Page(Label('<p>Hello World</p>'))
    )))

@Navigate.register
def end(origin):
    return Branch(Page(Label('<p>Goodbye World</p>'), terminal=True))
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

We'll open two terminal windows. In the first, run:

```
$ rq worker hemlock-task-queue
```

In the second, run:

```
$ python app.py # or python3 app.py
```

Open your browser to <http://localhost:5000>. Click the forward button and
notice that the Redis queue handles the navigate function.

####Methods



<p class="func-header">
    <i></i> <b>compile</b>(<i>page</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/workers.py#L76">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page</i></b>
<p class="attr">
    Page to which the worker is added.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>page : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>validate</b>(<i>page</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/workers.py#L90">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page</i></b>
<p class="attr">
    Page to which the worker is added.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>page : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>submit</b>(<i>page</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/workers.py#L104">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page</i></b>
<p class="attr">
    Page to which the worker is added.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>page : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>navigate</b>(<i>parent</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/workers.py#L118">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>parent : <i>hemlock.Branch or hemlock.Page</i></b>
<p class="attr">
    Branch or page to which the worker is added.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>parent : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**CompileWorker**



Handles a page's compile method.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
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



Handles a page's validate method.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
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



Handles a page's submit method.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
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
    <i>class</i> hemlock.<b>NavigateWorker</b>(<i>parent=None, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/workers.py#L214">[source]</a>
</p>

Handles a branch's or page's navigate method.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
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

