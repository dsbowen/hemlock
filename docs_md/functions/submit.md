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
</style># Submit functions

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.submit.**correct_choices**

<p class="func-header">
    <i>def</i> hemlock.functions.submit.<b>correct_choices</b>(<i>question, *values</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/submit.py#L9">[source]</a>
</p>

Convert the question's data to a 0-1 indicator that the participant
selected the correct choice(s).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.ChoiceQuestion</i></b>
<p class="attr">
    
</p>
<b>*values : <i></i></b>
<p class="attr">
    Values of the correct choices.
</p></td>
</tr>
    </tbody>
</table>

####Notes

If the participant can only select one choice, indicate whether the
participant selected one of the correct choices.

####Examples

```python
from hemlock import Check, Submit as S, push_app_context

app = push_app_context()

check = Check(
    '<p>Select the correct choice.</p>',
    ['correct', 'incorrect', 'also incorrect'],
    submit=S.correct_choices('correct')
)
check.response = check.choices[0]
check._submit().data
```

Out:

```
1
```

##hemlock.functions.submit.**data_type**

<p class="func-header">
    <i>def</i> hemlock.functions.submit.<b>data_type</b>(<i>question, new_type, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/submit.py#L51">[source]</a>
</p>

Convert the quesiton's data to a new type. If the question's data cannot
be converted, it is changed to `None`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>new_type : <i>class</i></b>
<p class="attr">
    
</p>
<b>*args, **kwargs : <i></i></b>
<p class="attr">
    Arguments and keyword arguments to pass to the <code>new_type</code> constructor.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Submit as S, push_app_context

app = push_app_context()

inpt = Input(data='1', submit=S.data_type(int))
inpt._submit()
inpt.data, isinstance(inpt.data, int)
```

Out:

```
(1, True)
```

##hemlock.functions.submit.**match**

<p class="func-header">
    <i>def</i> hemlock.functions.submit.<b>match</b>(<i>question, pattern</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/submit.py#L88">[source]</a>
</p>

Convert the question's data to a 0-1 indicator that the data matches the
pattern.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>pattern : <i>str or hemlock.Question</i></b>
<p class="attr">
    Regex pattern to match. If this is a <code>Question</code>, the pattern is the question's <code>response</code>'.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Submit as S, push_app_context

app = push_app_context()

inpt = Input(data='hello world', submit=S.match('hello *'))
inpt._submit().data
```

Out:

```
1
```

##hemlock.functions.submit.**eq**

<p class="func-header">
    <i>def</i> hemlock.functions.submit.<b>eq</b>(<i>question, value, data_type=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/submit.py#L123">[source]</a>
</p>

Convert the question's data to a 0-1 indicator that the question's data
equals the given value.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>value : <i></i></b>
<p class="attr">
    Value that the data should equal. If a <code>Question</code>, then <code>value.data</code> is used.
</p>
<b>data_type : <i>class or None, default=None</i></b>
<p class="attr">
    Expected type of data. If <code>None</code>, the type of <code>value</code> will be used.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Submit as S, push_app_context

app = push_app_context()

inpt = Input(data=50, submit=S.eq(50))
inpt._submit()
inpt.data
```

Out:

```
1
```

##hemlock.functions.submit.**neq**

<p class="func-header">
    <i>def</i> hemlock.functions.submit.<b>neq</b>(<i>question, value, data_type=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/submit.py#L161">[source]</a>
</p>

Convert the question's data to a 0-1 indicator that the question's data
does not equal the given value.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>value : <i></i></b>
<p class="attr">
    Value that the data should not equal. If a <code>Question</code>, then <code>value.data</code> is used.
</p>
<b>data_type : <i>class or None, default=None</i></b>
<p class="attr">
    Expected type of data. If <code>None</code>, the type of <code>value</code> will be used.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Submit as S, push_app_context

app = push_app_context()

inpt = Input(data=50, submit=S.neq(50))
inpt._submit()
inpt.data
```

Out:

```
0
```

##hemlock.functions.submit.**max**

<p class="func-header">
    <i>def</i> hemlock.functions.submit.<b>max</b>(<i>question, max, data_type=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/submit.py#L199">[source]</a>
</p>

Convert the question's data to a 0-1 indicator that the question's data
is less than the maximum value.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>max : <i></i></b>
<p class="attr">
    Maximum value. If a <code>Question</code>, then <code>max.data</code> is used.
</p>
<b>data_type : <i>class or None, default=None</i></b>
<p class="attr">
    Expected type of data. If <code>None</code>, the type of <code>max</code> will be used.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Submit as S, push_app_context

app = push_app_context()

inpt = Input(data=101, submit=S.max(100))
inpt._submit()
inpt.data
```

Out:

```
0
```

##hemlock.functions.submit.**min**

<p class="func-header">
    <i>def</i> hemlock.functions.submit.<b>min</b>(<i>question, min, data_type=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/submit.py#L236">[source]</a>
</p>

Convert the question's data to a 0-1 indicator that the question's data
is greater than the minimum value.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>min : <i></i></b>
<p class="attr">
    Minimum value. If a <code>Question</code>, then <code>min.data</code> is used.
</p>
<b>data_type : <i>class or None, default=None</i></b>
<p class="attr">
    Expected type of data. If <code>None</code>, the type of <code>min</code> will be used.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Submit as S, push_app_context

app = push_app_context()

inpt = Input(data=-1, submit=S.min(0))
inpt._submit()
inpt.data
```

Out:

```
0
```

##hemlock.functions.submit.**range**

<p class="func-header">
    <i>def</i> hemlock.functions.submit.<b>range</b>(<i>question, min, max, data_type=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/submit.py#L273">[source]</a>
</p>

Convert the question's data to a 0-1 indicator that the question's data
is within the range of `[min, max]`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>min : <i></i></b>
<p class="attr">
    Minimum value. If a <code>Question</code>, then <code>min.data</code> is used.
</p>
<b>max : <i></i></b>
<p class="attr">
    Maximum value. If a <code>Question</code>, then <code>max.data</code> is used.
</p>
<b>data_type : <i>class or None, default=None</i></b>
<p class="attr">
    Expected type of data. If <code>None</code>, the type of <code>min</code> and <code>max</code> will be used.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Submit as S, push_app_context

app = push_app_context()

inpt = Input(data=50, submit=S.range(0, 100))
inpt._submit()
inpt.data
```

Out:

```
1
```