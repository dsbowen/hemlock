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
</style># Application factory and settings

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.app.**push_app_context**

<p class="func-header">
    <i>def</i> hemlock.app.<b>push_app_context</b>(<i></i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/app/__init__.py#L42">[source]</a>
</p>

Push an app context for debugging in shell or notebook.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>app : <i>flask.app.Flask</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import push_app_context

app = push_app_context()
```

Out:

```
<Flask 'hemlock.app'>
```

##hemlock.app.**create_app**

<p class="func-header">
    <i>def</i> hemlock.app.<b>create_app</b>(<i>settings=settings</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/app/__init__.py#L73">[source]</a>
</p>

Create a Hemlock application.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>settings : <i>dict</i></b>
<p class="attr">
    Default settings for the application, extensions, and models.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>app : <i>flask.app.Flask</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Examples

In this example, we add a back button to every page in our survey.

```python
from hemlock import Page, create_app, settings

settings['Page'].update({'back': True})

app = create_app()
app.app_context().push()
Page().preview()
```



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

