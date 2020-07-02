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
</style># Validation functions

These are built-in functions to validate a participant's response to a
question. They return `None` if the response is valid, and an error message if
the repsonse is invalid.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.validate.**is_type**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>is_type</b>(<i>question, resp_type</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L19">[source]</a>
</p>

Validate that the response can be converted to a given type.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>resp_type : <i>class</i></b>
<p class="attr">
    The required type of response.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='hello world')
Validate.is_type(inpt, float)
inpt._validate()
inpt.error
```

Out:

```
Please enter a number.
```

##hemlock.functions.validate.**require**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>require</b>(<i>question</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L62">[source]</a>
</p>

Require a response to this question.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response=None)
Validate.require(inpt)
inpt._validate()
inpt.error
```

Out:

```
Please respond to this question.
```

##hemlock.functions.validate.**is_in**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>is_in</b>(<i>question, valid_set, resp_type=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L96">[source]</a>
</p>

Validate that the question response is in a set of valid responses.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>valid_set : <i>iterable</i></b>
<p class="attr">
    Set of valid responses.
</p>
<b>resp_type : <i>class or None, default=None</i></b>
<p class="attr">
    Type of response expected; should match the type of elements in <code>valid_set</code>.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='earth')
Validate.is_in(inpt, ('wind', 'fire'))
inpt._validate()
inpt.error
```

Out:

```
Please enter wind or fire.
```

##hemlock.functions.validate.**is_not_in**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>is_not_in</b>(<i>question, invalid_set, resp_type=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L137">[source]</a>
</p>

Validate that the question response is *not* in a set of invalid
responses.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>invalid_set : <i>iterable</i></b>
<p class="attr">
    Set of invalid responses.
</p>
<b>resp_type : <i>class or None, default=None</i></b>
<p class="attr">
    Type of response expected; should match the type of elements in <code>invalid_set</code>.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='earth')
Validate.is_not_in(inpt, ['earth', 'wind', 'fire'])
inpt._validate()
inpt.error
```

Out:

```
Please do not enter earth, wind, or fire.
```

##hemlock.functions.validate.**max_val**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>max_val</b>(<i>question, max_, resp_type=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L181">[source]</a>
</p>

Validate that the response does not exceed a maximum value.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>max_ : <i></i></b>
<p class="attr">
    Maximum value.
</p>
<b>resp_type : <i>class or None, default=None</i></b>
<p class="attr">
    Expected type of response. If <code>None</code>, the type of <code>max</code> will be used.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='101')
Validate.max_val(inpt, 100)
inpt._validate()
inpt.error
```

Out:

```
Please enter a response less than 100.
```

##hemlock.functions.validate.**min_val**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>min_val</b>(<i>question, min_, resp_type=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L220">[source]</a>
</p>

Validate that the response does not deceed a minumum value.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>min_ : <i></i></b>
<p class="attr">
    Minimum value.
</p>
<b>resp_type : <i>class or None, default=None</i></b>
<p class="attr">
    Expected type of response. If <code>None</code>, the type of <code>min</code> will be used.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='-1')
Validate.min_val(inpt, 0)
inpt._validate()
inpt.error
```

Out:

```
Please enter a response greater than 0.
```

##hemlock.functions.validate.**range_val**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>range_val</b>(<i>question, min_, max_, resp_type=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L287">[source]</a>
</p>

Validate that the response is in a given range.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>min_ : <i></i></b>
<p class="attr">
    Minimum value for the question response.
</p>
<b>max_ : <i></i></b>
<p class="attr">
    Maximum value for the question response.
</p>
<b>resp_type : <i>class or None, default=None</i></b>
<p class="attr">
    Expected type of response. If <code>None</code>, the expected response type is the type of <code>min</code> and <code>max</code>, which must be of the same type.
</p>
<b>Out : <i></i></b>
<p class="attr">
    
</p>
<b>```python : <i></i></b>
<p class="attr">
    from hemlock import Input, Validate, push_app_context
</p>
<b>push_app_context() : <i></i></b>
<p class="attr">
    
</p>
<b>inpt = Input(response='101') : <i></i></b>
<p class="attr">
    Validate.range_val(inpt, 0, 100) inpt._validate() inpt.error ```
</p>
<b>Out : <i></i></b>
<p class="attr">
    
</p>
<b>``` : <i></i></b>
<p class="attr">
    Please enter a response between 0 and 100. ```
</p></td>
</tr>
    </tbody>
</table>



##hemlock.functions.validate.**exact_len**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>exact_len</b>(<i>question, len_</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L339">[source]</a>
</p>

Validates the exact length of the repsonse. For a string response, this is
the length of the string. For a choices response, this is the number of
choices selected.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>len_ : <i>int</i></b>
<p class="attr">
    Required length of the response.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='hello world')
Validate.exact_len(inpt, 5)
inpt._validate()
inpt.error
```

Out:

```
Please enter a response exactly 5 characters long.
```

##hemlock.functions.validate.**max_len**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>max_len</b>(<i>question, max_</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L384">[source]</a>
</p>

Validates the maximum length of the response. For a string response, this
is the length of the string. For a choices response, this is the number of
choices selected.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>max_ : <i>int</i></b>
<p class="attr">
    Maximum length of the response.
</p></td>
</tr>
    </tbody>
</table>

####Notes

A response of `None` is assumed to satisfy the max length validation. Use
`Validate.require` to require a response that is not `None`.

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='hello world')
Validate.max_len(inpt, 5)
inpt._validate()
inpt.error
```

Out:

```
Please enter a response at most 5 characters long.
```

##hemlock.functions.validate.**min_len**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>min_len</b>(<i>question, min_</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L433">[source]</a>
</p>

Valiadates the minimum length of the response. For a string response, this
is the length of the string. For a choices response, this is the number of
choices selected.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>min_ : <i>int</i></b>
<p class="attr">
    Minimum length of the response.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='hello world')
Validate.min_len(inpt, 15)
inpt._validate()
inpt.error
```

Out:

```
Please enter a response at least 15 characters long.
```

##hemlock.functions.validate.**range_len**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>range_len</b>(<i>question, min_, max_</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L480">[source]</a>
</p>

Validates the range of the response length. For a string response, this is
the length of the string. For a choices response, this is the number of
choices selected.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>min_ : <i>int</i></b>
<p class="attr">
    Minimum response length.
</p>
<b>max_ : <i>int</i></b>
<p class="attr">
    Maximum response length.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='hello world')
Validate.range_len(inpt, 5, 10)
inpt._validate()
inpt.error
```

Out:

```
Please enter a response 5 to 10 characters long.
```

##hemlock.functions.validate.**exact_words**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>exact_words</b>(<i>question, nwords</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L531">[source]</a>
</p>

Validate the exact number of words in the response.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>nwords : <i>int</i></b>
<p class="attr">
    Required number of words.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='hello world')
Validate.exact_words(inpt, 1)
inpt._validate()
inpt.error
```

Out:

```
Please enter exactly 1 word.
```

##hemlock.functions.validate.**max_words**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>max_words</b>(<i>question, max_</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L572">[source]</a>
</p>

Validates the maximum number of words in the response.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>max_ : <i>int</i></b>
<p class="attr">
    Maximum number of words.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='hello world')
Validate.max_words(inpt, 1)
inpt._validate()
inpt.error
```

Out:

```
Please enter at most 1 word.
```

##hemlock.functions.validate.**min_words**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>min_words</b>(<i>question, min_</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L611">[source]</a>
</p>

Validates the minimum number of words in the repsonse.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>min_ : <i>int</i></b>
<p class="attr">
    Minimum number of words.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='hello world')
Validate.min_words(inpt, 3)
inpt._validate()
inpt.error
```

Out:

```
Please enter at least 3 words.
```

##hemlock.functions.validate.**range_words**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>range_words</b>(<i>question, min_, max_</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L653">[source]</a>
</p>

Validates the number of words falls in a given range.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>min_ : <i>int</i></b>
<p class="attr">
    Minumum number of words.
</p>
<b>max_ : <i>int</i></b>
<p class="attr">
    Maximum number of words.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='hello world')
Validate.range_words(inpt, 3, 5)
inpt._validate()
inpt.error
```

Out:

```
Please enter between 3 and 5 words.
```

##hemlock.functions.validate.**exact_decimals**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>exact_decimals</b>(<i>question, ndec</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L704">[source]</a>
</p>

Validates the exact number of decimals.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>ndec : <i>int</i></b>
<p class="attr">
    Required number of decimals.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='1')
Validate.exact_decimals(inpt, 2)
inpt._validate()
inpt.error
```

Out:

```
Please enter a number with exactly 2 decimals.
```

##hemlock.functions.validate.**max_decimals**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>max_decimals</b>(<i>question, max_</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L743">[source]</a>
</p>

Validates the maximum number of decimals.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>max_ : <i>int</i></b>
<p class="attr">
    Maximum number of decimals.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='1.123')
Validate.max_decimals(inpt, 2)
inpt._validate()
inpt.error
```

Out:

```
Please enter a number with at most 2 decimals.
```

##hemlock.functions.validate.**min_decimals**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>min_decimals</b>(<i>question, min_</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L782">[source]</a>
</p>

Validates the minumum number of decimals.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>min_ : <i>int</i></b>
<p class="attr">
    Minumum number of decimals.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='1')
Validate.min_decimals(inpt, 2)
inpt._validate()
inpt.error
```

Out:

```
Please enter a number with at least 2 decimals.
```

##hemlock.functions.validate.**range_decimals**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>range_decimals</b>(<i>question, min_, max_</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L821">[source]</a>
</p>

Validates the number of decimals are in a given range.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>min_ : <i>int</i></b>
<p class="attr">
    Minimum number of decimals.
</p>
<b>max_ : <i>int</i></b>
<p class="attr">
    Maximum number of decimals.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='1.123')
Validate.range_decimals(inpt, 0, 2)
inpt._validate()
inpt.error
```

Out:

```
Please enter a number with 0 to 2 decimals.
```

##hemlock.functions.validate.**match**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>match</b>(<i>question, pattern</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L878">[source]</a>
</p>

Validate that the response matches the regex pattern.

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
from hemlock import Input, Validate, push_app_context

push_app_context()

inpt = Input(response='hello world')
Validate.match(inpt, 'goodbye *')
inpt._validate()
inpt.error
```

Out:

```
Please enter a response with the correct pattern.
```

##hemlock.functions.validate.**correct_choices**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>correct_choices</b>(<i>question, *correct</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L914">[source]</a>
</p>

Validate that selected choice(s) is correct.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>*correct : <i></i></b>
<p class="attr">
    Correct choices.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Check, Validate, push_app_context

push_app_context()

check = Check(choices=['correct','incorrect','also incorrect'])
Validate.correct_choices(check, check.choices[0])
check.response = check.choices[1]
check._validate()
check.error
```

Out:

```
Please select the correct choice.
```