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

You can input a custom error message for any of these functions by passing a
keyword parameter `error_msg`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.validate.**is_type**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>is_type</b>(<i>question, resp_type, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L22">[source]</a>
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



##hemlock.functions.validate.**require**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>require</b>(<i>question, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L49">[source]</a>
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



##hemlock.functions.validate.**is_in**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>is_in</b>(<i>question, valid_set, resp_type=None, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L65">[source]</a>
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



##hemlock.functions.validate.**is_not_in**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>is_not_in</b>(<i>question, invalid_set, resp_type=None, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L89">[source]</a>
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



##hemlock.functions.validate.**max_val**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>max_val</b>(<i>question, max, resp_type=None, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L116">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.validate.**min_val**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>min_val</b>(<i>question, min, resp_type=None, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L123">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.validate.**range_val**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>range_val</b>(<i>question, min, max, resp_type=None, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L158">[source]</a>
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
<b>min : <i></i></b>
<p class="attr">
    Minimum value for the question response.
</p>
<b>max : <i></i></b>
<p class="attr">
    Maximum value for the question response.
</p>
<b>resp_type : <i>class or None, default=None</i></b>
<p class="attr">
    Expected type of response. If <code>None</code>, the expected response type is the type of <code>min</code> and <code>max</code>, which must be of the same type.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.functions.validate.**exact_len**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>exact_len</b>(<i>question, len_, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L190">[source]</a>
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



##hemlock.functions.validate.**max_len**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>max_len</b>(<i>question, max, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L218">[source]</a>
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
<b>max : <i>int</i></b>
<p class="attr">
    Maximum length of the response.
</p></td>
</tr>
    </tbody>
</table>

####Notes

A response of `None` is assumed to satisfy the max length validation. Use
`Validate.require` to require a response that is not `None`.

##hemlock.functions.validate.**min_len**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>min_len</b>(<i>question, min, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L250">[source]</a>
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
<b>min : <i>int</i></b>
<p class="attr">
    Minimum length of the response.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.functions.validate.**range_len**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>range_len</b>(<i>question, min, max, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L278">[source]</a>
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
<b>min : <i>int</i></b>
<p class="attr">
    Minimum response length.
</p>
<b>max : <i>int</i></b>
<p class="attr">
    Maximum response length.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.functions.validate.**exact_words**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>exact_words</b>(<i>question, nwords, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L310">[source]</a>
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



##hemlock.functions.validate.**max_words**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>max_words</b>(<i>question, max, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L335">[source]</a>
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
<b>max : <i>int</i></b>
<p class="attr">
    Maximum number of words.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.functions.validate.**min_words**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>min_words</b>(<i>question, min, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L355">[source]</a>
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
<b>min : <i>int</i></b>
<p class="attr">
    Minimum number of words.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.functions.validate.**range_words**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>range_words</b>(<i>question, min, max, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L376">[source]</a>
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
<b>min : <i>int</i></b>
<p class="attr">
    Minumum number of words.
</p>
<b>max : <i>int</i></b>
<p class="attr">
    Maximum number of words.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.functions.validate.**exact_decimals**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>exact_decimals</b>(<i>question, ndec, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L406">[source]</a>
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



##hemlock.functions.validate.**max_decimals**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>max_decimals</b>(<i>question, max, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L426">[source]</a>
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
<b>max : <i>int</i></b>
<p class="attr">
    Maximum number of decimals.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.functions.validate.**min_decimals**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>min_decimals</b>(<i>question, min, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L449">[source]</a>
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
<b>min : <i>int</i></b>
<p class="attr">
    Minumum number of decimals.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.functions.validate.**range_decimals**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>range_decimals</b>(<i>question, min, max, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L472">[source]</a>
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
<b>min : <i>int</i></b>
<p class="attr">
    Minimum number of decimals.
</p>
<b>max : <i>int</i></b>
<p class="attr">
    Maximum number of decimals.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.functions.validate.**match**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>match</b>(<i>question, pattern, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L510">[source]</a>
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



##hemlock.functions.validate.**correct_choices**

<p class="func-header">
    <i>def</i> hemlock.functions.validate.<b>correct_choices</b>(<i>question, *correct, error_msg=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/validate.py#L527">[source]</a>
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

