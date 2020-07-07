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
</style>## Compile functions

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.compile.**call_method**

<p class="func-header">
    <i>def</i> hemlock.functions.compile.<b>call_method</b>(<i>obj, method_name, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/compile.py#L7">[source]</a>
</p>

Calls one of the object's methods.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>obj : <i></i></b>
<p class="attr">
    Object whose methods will be called.
</p>
<b>method_name : <i>str</i></b>
<p class="attr">
    Names of the method to call.
</p>
<b>*args, **kwargs : <i></i></b>
<p class="attr">
    Arguments and keyword arguments to pass to the method.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Compile, Page, push_app_context

push_app_context()

p = Compile.call_method(Page(error='Error message'), 'clear_error')
p.preview() # p.preview('Ubuntu') if running in Ubuntu/WSL
p._compile()
p.preview()
```

##hemlock.functions.compile.**clear_error**

<p class="func-header">
    <i>def</i> hemlock.functions.compile.<b>clear_error</b>(<i>obj</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/compile.py#L38">[source]</a>
</p>

Calls the object's `clear_error` method.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>obj : <i></i></b>
<p class="attr">
    Object whose <code>clear_error</code> method will be called.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Compile, Page, Check, push_app_context

push_app_context()

p = Compile.clear_error(Page(error='Error message'))
p.preview() # p.preview('Ubuntu') if running in Ubuntu/WSL
p._compile()
p.preview()
```

##hemlock.functions.compile.**clear_response**

<p class="func-header">
    <i>def</i> hemlock.functions.compile.<b>clear_response</b>(<i>obj</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/compile.py#L63">[source]</a>
</p>

Calls the object's `clear_response` method.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>obj : <i></i></b>
<p class="attr">
    Object whose <code>clear_response</code> method will be called.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Compile, Input, Page, push_app_context

push_app_context()

p = Compile.clear_response(Page(Input(response='Hello World')))
p.preview() # p.preview('Ubuntu') if running in Ubuntu/WSL
p._compile()
p.preview()
```

##hemlock.functions.compile.**shuffle**

<p class="func-header">
    <i>def</i> hemlock.functions.compile.<b>shuffle</b>(<i>obj, *attrs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/compile.py#L88">[source]</a>
</p>

Shuffle an object's attributes.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>obj : <i></i></b>
<p class="attr">
    Objects whose attributes should be shuffled.
</p>
<b>*attrs : <i>str</i></b>
<p class="attr">
    Names of attributes to shuffle.
</p></td>
</tr>
    </tbody>
</table>

####Notes

If the object is a `hemlock.Page`, the default shuffled attribute is its
`questions`.

If the object is a `hemlock.ChoiceQuestion`, the default shuffled
attribute is its `choices`.

####Examples

```python
from hemlock import Compile, Label, Page, push_app_context

push_app_context()

p = Compile.shuffle(Page(
    Label('<p>Label {}</p>'.format(i)) for i in range(4)
))
p.preview() # p.preview('Ubuntu') if running in Ubuntu/WSL
p._compile()
p.preview()
```