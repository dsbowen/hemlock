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
    <i>def</i> hemlock.functions.submit.<b>correct_choices</b>(<i>question, *values</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/submit.py#L8">[source]</a>
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
    <i>def</i> hemlock.functions.submit.<b>data_type</b>(<i>question, new_type, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/submit.py#L50">[source]</a>
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
    <i>def</i> hemlock.functions.submit.<b>match</b>(<i>question, pattern</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/submit.py#L87">[source]</a>
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
<b>pattern : <i>str</i></b>
<p class="attr">
    Regex pattern to match.
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