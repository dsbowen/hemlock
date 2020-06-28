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
</style># Debug functions

Users will likely rely most on the following debug functions.

Page debugging:
1. `forward`. Navigate forward.
2. `back`. Navigate backward.
3. `navigate`. Navigate in a random direction (or refresh the page)

Textarea and Input debugging:
1. `send_keys`. Send specified keys to the input (or textarea) tag.

Choice question debugging:
1. `click_choices`. Click on the input choices.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



## Page debugging

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**forward**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>forward</b>(<i>driver, page</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L30">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**back**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>back</b>(<i>driver, page</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L34">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**navigate**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>navigate</b>(<i>driver, page, p_forward=0.8, p_back=0.1, sleep_time=3</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L38">[source]</a>
</p>

Navigate randomly

This method randomly navigates forward or backward, or refreshes the
page.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**debug_func**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>debug_func</b>(<i>driver, page</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L60">[source]</a>
</p>

Run the question debug functions in random order

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**settings**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>settings</b>(<i>'Page') def settings(</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L66">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



Textarea and text Input debugging

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**send_keys**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>send_keys</b>(<i>driver, question, keys, p_exec=1</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L71">[source]</a>
</p>

Send keys method

This debugger sends the specified keys or list or keys to the textarea
or input.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**random_str**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>random_str</b>(<i>driver, question, magnitude=2, p_whitespace=0.2</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L90">[source]</a>
</p>

Random string

This debugger sends a random string to the textarea. `magnitude` is the
maximum magnitude of the length of the string. `p_whitespace` is the
probability of sending a whitespace character.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**random_number**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>random_number</b>(<i>driver, question, p_exec=1, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L105">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**gen_number**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>gen_number</b>(<i>integer=False, magnitude_lb=0, magnitude_ub=10, p_negative= 0.1, max_decimals=5</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L111">[source]</a>
</p>

Generate a random number

`magnitude_lb` and `magnitude_ub` specify the lower and upper bound on
the mangitude of the number.
`p_negative` is the probability of generating a random number.
`max_decimals` is the maximum number of decimals to which the number
can be rounded.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**random_keys**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>random_keys</b>(<i>driver, question, p_str=0.5, p_int=0.25</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L130">[source]</a>
</p>

Send random keys

This method sends random keys to a textarea or input.

With probability `p_skip`, this method skips the question without sending keys.
With probability `p_str`, this method sends a random string.
With probability `p_int`, this method sends an integer.
Otherwise, it sends a floating point number.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**default_textarea_debug**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>default_textarea_debug</b>(<i>driver, question, p_skip=0.1</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L146">[source]</a>
</p>

Skip or send random string

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**settings**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>settings</b>(<i>'Textarea') def settings(</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L152">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



Date and time input

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**random_date**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>random_date</b>(<i>driver, question, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L157">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**random_datetime**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>random_datetime</b>(<i>driver, question, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L162">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**random_month**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>random_month</b>(<i>driver, question, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L169">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**random_time**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>random_time</b>(<i>driver, question, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L175">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**random_week**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>random_week</b>(<i>driver, question, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L180">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**gen_datetime**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>gen_datetime</b>(<i>p_future=0.5, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L185">[source]</a>
</p>

Randomly generate datetime

This method randomly generates a datetime object by subtracting a
timedelta from the current datetime. The timedelta's seconds are
determined by the random number generator specified above.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



Default input debugger

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**default_input_debug**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>default_input_debug</b>(<i>driver, question, p_skip=0.1</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L206">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**settings**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>settings</b>(<i>'Input') def settings(</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L212">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



Range debugger

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**drag_range**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>drag_range</b>(<i>driver, question, xoffset=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L219">[source]</a>
</p>

Drag the range slider to xoffset

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**settings**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>settings</b>(<i>'Range') def settings(</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L226">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



Choice question debugger

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**click_choices**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>click_choices</b>(<i>driver, question, *choices, p_exec=1</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L231">[source]</a>
</p>

Click on input choices

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**clear_choices**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>clear_choices</b>(<i>driver, question, p_exec=1</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L242">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**default_choice_question_debug**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>default_choice_question_debug</b>(<i>driver, question, p_skip=0.1</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L257">[source]</a>
</p>

Default choice question debugging function

This method randomly selects choices to click on. The number of choices
to click on is a random number from 0 to len(question.choices).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.functions.debug.**settings**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>settings</b>(<i>'ChoiceQuestion') def settings(</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L272">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

