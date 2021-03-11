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
</style># Function column types

All of these classes inherit from
[`sqlalchemy_mutable.partial`](https://dsbowen.github.io/sqlalchemy-mutable).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Compile**



Helps compile a page or question html before it is rendered and displayed
to a participant.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

####Examples

```python
from hemlock import Compile as C, Input, Label, Page, push_app_context

app = push_app_context()

@C.register
def greet(greet_q, name_q):
    greet_q.label = f'Hello {name_q.response}!'

name_q = Input("What's your name?")
p = Page(Label(compile=C.greet(name_q)))
name_q.response = 'World'
p._compile()
p.preview()
```



##hemlock.**Debug**

<p class="func-header">
    <i>class</i> hemlock.<b>Debug</b>(<i>func, *args, p_exec=1.0, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L37">[source]</a>
</p>

Run to help debug the survey.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
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

p = Page(Input('Enter a greeting.', debug=D.greet()))
p.debug.pop(-1) # so the page won't navigate
p.preview(driver)
p._debug(driver)
```

####Methods



<p class="func-header">
    <i></i> <b>__call__</b>(<i>self, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L67">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Validate**

<p class="func-header">
    <i>class</i> hemlock.<b>Validate</b>(<i>func, *args, error_msg=None, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L72">[source]</a>
</p>

Validates a participant's response.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>error_msg : <i>str or None</i></b>
<p class="attr">
    If the validate function returns an error message, <code>error_msg</code> is returned instead of the output of the validate function. You can set this by passing in an <code>error_msg</code> keyword argument to the constructor.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate as V, push_app_context

app = push_app_context()

@V.register
def match(inpt, pattern):
    if inpt.response != pattern:
        return f'You entered "{inpt.response}", not "{pattern}"'

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
    <i></i> <b>__call__</b>(<i>self, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L113">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Submit**



Runs after a participant has successfully submitted a page.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
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

inpt = Input("What's your name?", submit=S.get_initials())
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

