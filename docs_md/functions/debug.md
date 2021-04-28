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

Debug functions tell the AI participant what to do during debugging. They
generally take a selenium webdriver as their first argument and a page or
question as their second argument.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

####Notes

The following examples open a webdriver. After running the examples, close the
driver with `driver.close()`.

By default, the last debug function of a page navigates. To remove this, run
`page.debug.pop()`.

##hemlock.functions.debug.**forward**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>forward</b>(<i>driver, page, max_wait=30, wait_interval=3</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L59">[source]</a>
</p>

Click the forward button.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>page : <i>hemlock.Page</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Debug as D, Page, push_app_context
from hemlock.tools import chromedriver

app = push_app_context()

driver = chromedriver()

p = Page(
    debug=[D.debug_questions(), D.forward()]
)
p.preview(driver)
p._debug(driver)
```

##hemlock.functions.debug.**back**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>back</b>(<i>driver, page, max_wait=30, wait_interval=1</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L93">[source]</a>
</p>

Click the back button.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>page : <i>hemlock.Page</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Debug as D, Page, push_app_context
from hemlock.tools import chromedriver

app = push_app_context()

driver = chromedriver()

p = Page(
    debug=[D.debug_questions(), D.back()]
)
p.preview(driver)
p._debug(driver)
```

##hemlock.functions.debug.**send_keys**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>send_keys</b>(<i>driver, question, *keys, p_num=0.5</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L129">[source]</a>
</p>

Send the specified keys to the `<textarea>` or `<input>`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>*keys : <i></i></b>
<p class="attr">
    Keys to send to the textarea or input. If empty, keys are randomly selected.
</p>
<b>p_num : <i>float, default=.5</i></b>
<p class="attr">
    Probability of sending a random number if keys are not specified (as opposed to a random string).
</p></td>
</tr>
    </tbody>
</table>

####Notes

This debug function is skipped if the question is not displayed.

####Examples

```python
from hemlock import Debug as D, Input, Page, push_app_context
from hemlock.tools import chromedriver

app = push_app_context()

driver = chromedriver()

p = Page(
    Input(debug=D.send_keys('hello world')),
    debug=D.debug_questions()
)
p.preview(driver)
p._debug(driver)
```

##hemlock.functions.debug.**send_datetime**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>send_datetime</b>(<i>driver, question, datetime_=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L194">[source]</a>
</p>

Send a `datetime.datetime` object to an input. Inputs should be of type
'date', 'datetime-local', 'month', 'time', or 'week',

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>question : <i>hemlock.Question</i></b>
<p class="attr">
    
</p>
<b>datetime_ : <i>datetime.datetime or None, default=None</i></b>
<p class="attr">
    The datetime object to send. If <code>None</code>, a date and time are chosen randomly.
</p></td>
</tr>
    </tbody>
</table>

####Notes

This debug function is skipped if the question is not displayed.

####Examples

```python
from hemlock import Debug as D, Input, Page, push_app_context
from hemlock.tools import chromedriver

from datetime import datetime

app = push_app_context()

driver = chromedriver()

p = Page(
    Input(type='date', debug=D.send_datetime(datetime.utcnow())),
    debug=D.debug_questions()
)
p.preview(driver)
p._debug(driver)
```

##hemlock.functions.debug.**random_input**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>random_input</b>(<i>driver, question</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L239">[source]</a>
</p>

Default debug function for input questions. This function sends a random
string or number if the input takes text, or a random `datetime.datetime`
object if the input takes dates or times.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>question : <i>hemlock.Input</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.functions.debug.**click_slider_range**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>click_slider_range</b>(<i>driver, slider, target=None, tol=0, max_iter=10, max_wait=3, wait_interval=1</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L266">[source]</a>
</p>

Click a Bootstrap-slider input.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>slider : <i>hemlock.Slider</i></b>
<p class="attr">
    
</p>
<b>target : <i>float or None, default=None</i></b>
<p class="attr">
    Target value to which the slider should be dragged. If <code>None</code>, a random target value will be chosen.
</p>
<b>tol : <i>float, default=0</i></b>
<p class="attr">
    Tolerance for error if the slider cannot be dragged to the exact target.
</p>
<b>max_iter : <i>int, default=10</i></b>
<p class="attr">
    Maximum number of iterations for the slider to reach the target.
</p>
<b>max_wait : <i>int, default=3</i></b>
<p class="attr">
    Number of iterations to wait for javascript to load the slider.
</p>
<b>wait_interval : <i>int, default=1</i></b>
<p class="attr">
    Number of seconds to wait each iteration.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Debug as D, Page, Slider, push_app_context
from hemlock.tools import chromedriver

app = push_app_context()

driver = chromedriver()

p = Page(
    Slider(debug=D.click_slider_range(80)),
    debug=D.debug_questions()
)
p.preview(driver)
p._debug(driver)
```

##hemlock.functions.debug.**drag_range**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>drag_range</b>(<i>driver, range_, target=None, tol=0, max_iter=10</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L333">[source]</a>
</p>

Drag a range slider to specified target value.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>range_ : <i>hemlock.Range</i></b>
<p class="attr">
    
</p>
<b>target : <i>float or None, default=None</i></b>
<p class="attr">
    Target value to which the slider should be dragged. If <code>None</code>, a random target value will be chosen.
</p>
<b>tol : <i>float, default=0</i></b>
<p class="attr">
    Tolerance for error if the slider cannot be dragged to the exact target.
</p>
<b>max_iter : <i>int, default=10</i></b>
<p class="attr">
    Maximum number of iterations for the slider to reach the target.
</p></td>
</tr>
    </tbody>
</table>

####Notes

This debug function is skipped if the question is not displayed.

####Examples

```python
from hemlock import Debug as D, Page, Range, push_app_context
from hemlock.tools import chromedriver

app = push_app_context()

driver = chromedriver()

p = Page(
    Range(debug=D.drag_range(80)),
    debug=D.debug_questions()
)
p.preview(driver)
p._debug(driver)
```

##hemlock.functions.debug.**click_choices**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>click_choices</b>(<i>driver, question, *values, if_selected=None, max_clicks=5</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L391">[source]</a>
</p>

Click on choices or options.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>question : <i>hemlock.ChoiceQuestion</i></b>
<p class="attr">
    
</p>
<b>*values : <i></i></b>
<p class="attr">
    Values of the choices on which to click. If no choices are specified, the debugger will click on random choices.
</p>
<b>if_selected : <i>bool or None, default=None</i></b>
<p class="attr">
    Indicates that the choices will be clicked only if they are already selected. If <code>False</code> the choices will be clicked only if they are not already selected. If <code>None</code> the choices will be clicked whether or not they are selected.
</p></td>
</tr>
    </tbody>
</table>

####Notes

Will not attempt to click choices or options which are not displayed.

####Examples

```python
from hemlock import Check, Debug as D, Page, push_app_context
from hemlock.tools import chromedriver

app = push_app_context()

driver = chromedriver()

p = Page(
    Check(
        '<p>Click "Yes".</p>',
        ['Yes', 'No', 'Maybe'],
        debug=D.click_choices('Yes')
    ),
    debug=D.debug_questions()
)
p.preview(driver)
p._debug(driver)
```

##hemlock.functions.debug.**clear_choices**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>clear_choices</b>(<i>driver, question</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L449">[source]</a>
</p>

Clear selected choices.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>question : <i>hemlock.ChoiceQuestion</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Notes

Intended only for questions in which multiple choices may be selected.

####Examples

```python
from hemlock import Check, Debug as D, Page, push_app_context
from hemlock.tools import chromedriver

app = push_app_context()

driver = chromedriver()

p = Page(
    Check(
        "<p>Which ice cream flavors do you like?</p>",
        ['Chocolate', 'Vanilla', 'Strawberry'],
        default='Chocolate',
        multiple=True,
        debug=D.clear_choices()
    ),
    debug=D.debug_questions()
)
p.preview(driver)
p._debug(driver)
```