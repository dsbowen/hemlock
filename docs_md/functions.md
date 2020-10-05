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
</style># Function models

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**FunctionRegistrar**



Mixin for Function models which provides a method for function
registration.

Inherits from
[`sqlalchemy_function.FunctionMixin`](<https://dsbowen.github.io/sqlalchemy-function/>).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>index : <i>int or None</i></b>
<p class="attr">
    Order in which this Function will be executed, relative to other Functions belonging to the same parent object.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>register</b>(<i>cls, func</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L34">[source]</a>
</p>

This decorator registers a function.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>func : <i>callable</i></b>
<p class="attr">
    The function to register.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**Compile**



Helps compile a page or question html before it is rendered and displayed
to a participant.

Inherits from `hemlock.FunctionRegistrar`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Page to which this model belongs.
</p>
<b>question : <i>hemlock.Question or None</i></b>
<p class="attr">
    Question to which this model belongs.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Compile as C, Input, Label, Page, push_app_context

app = push_app_context()

@C.register
def greet(greet_q, name_q):
    greet_q.label = '<p>Hello {}!</p>'.format(name_q.response)

name_q = Input("<p>What's your name?</p>")
p = Page(Label(compile=C.greet(name_q)))
name_q.response = 'World'
p._compile().preview()
```



##hemlock.**Debug**

<p class="func-header">
    <i>class</i> hemlock.<b>Debug</b>(<i>*args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L88">[source]</a>
</p>

Run to help debug the survey.

Inherits from `hemlock.FunctionRegistrar`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>p_exec : <i>float, default=1.</i></b>
<p class="attr">
    Probability that the debug function will execute. You can set this by passing in an <code>p_exec</code> keyword argument to the constructor.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Page to which this model belongs.
</p>
<b>question : <i>hemlock.Question or None</i></b>
<p class="attr">
    Question to which this model belongs.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Debug as D, Input, Page, push_app_context
from hemlock.tools import chromedriver

app = push_app_context()

driver = chromedriver()

@D.register
def greet(driver, greet_q):
    inpt = greet_q.input_from_driver(driver)
    inpt.clear()
    inpt.send_keys('Hello World!')

p = Page(Input('<p>Enter a greeting.</p>', debug=D.greet()))
p.debug.pop(-1) # so the page won't navigate
p.preview(driver)._debug(driver)
```

####Methods



<p class="func-header">
    <i></i> <b>__call__</b>(<i>self, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L138">[source]</a>
</p>

Execute the debug function with probability `self.p_exec`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Validate**

<p class="func-header">
    <i>class</i> hemlock.<b>Validate</b>(<i>*args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L146">[source]</a>
</p>

Validates a participant's response.

Inherits from `hemlock.FunctionRegistrar`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>error_msg : <i>str or None</i></b>
<p class="attr">
    If the validate function returns an error message, the <code>error_msg</code> attribute is returned instead of the output of the validate function. You can set this by passing in an <code>error_msg</code> keyword argument to the constructor.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Page to which this model belongs.
</p>
<b>question : <i>hemlock.Question or None</i></b>
<p class="attr">
    Question to which this model belongs.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate as V, push_app_context

app = push_app_context()

@Validate.register
def match(inpt, pattern):
    if inpt.response != pattern:
        return '<p>You entered "{}", not "{}"</p>'.format(inpt.response, pattern)

pattern = 'hello world'
inpt = Input(validate=V.match(pattern))
inpt.response = 'goodbye moon'
inpt._validate()
inpt.error
```

Out:

```
You entered "goodbye moon", not "hello world"
```

####Methods



<p class="func-header">
    <i></i> <b>__call__</b>(<i>self, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L202">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>error_msg : <i>str or None</i></b>
<p class="attr">
    Return <code>None</code> if there is no error. If there is an error, return <code>self.error_msg</code> or the output of <code>self.func</code>.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**Submit**



Runs after a participant has successfully submitted a page.

Inherits from `hemlock.FunctionRegistrar`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Page to which this model belongs.
</p>
<b>question : <i>hemlock.Question or None</i></b>
<p class="attr">
    Question to which this model belongs.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Submit as S, push_app_context

app = push_app_context()

@S.register
def get_initials(name_q):
    names = name_q.response.split()
    name_q.data = '.'.join([name[0] for name in names]) + '.'

inpt = Input("<p>What's your name?</p>", submit=S.get_initials())
inpt.response = 'Andrew Yang'
inpt._submit().data
```

Out:

```
A.Y.
```



##hemlock.**Navigate**



Creates a new branch to which the participant will navigate.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>branch : <i>hemlock.Branch or None</i></b>
<p class="attr">
    Branch to which this model belongs.
</p>
<b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Page to which this model belongs.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Branch, Navigate as N, Page, Participant, push_app_context

def start():
    return Branch(Page(), navigate=N.end())

@N.register
def end(start_branch):
    return Branch(Page(terminal=True))

app = push_app_context()

part = Participant.gen_test_participant(start)
part.view_nav()
```

Out:

```
<Branch 1>
<Page 1> C

C = current page
T = terminal page
```

In:

```python
part.forward().view_nav()
```

Out:

```
<Branch 1>
<Page 1>
    <Branch 2>
    <Page 2> C T

C = current page
T = terminal page
```

####Methods



<p class="func-header">
    <i></i> <b>__call__</b>(<i>self, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L317">[source]</a>
</p>

Create a new branch and 'link' it to the tree. Linking in the new
branch involves setting the `next_branch` and `origin_branch` or
`origin_page` relationships.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

