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
    <i>def</i> hemlock.functions.debug.<b>forward</b>(<i>driver, page</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L30">[source]</a>
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

p = Page(debug=[D.debug_questions(), D.forward()])
p.preview(driver)._debug(driver)
```

##hemlock.functions.debug.**back**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>back</b>(<i>driver, page</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L57">[source]</a>
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

p = Page(debug=[D.debug_questions(), D.back()])
p.preview(driver)._debug(driver)
```

##hemlock.functions.debug.**send_keys**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>send_keys</b>(<i>driver, question, *keys, p_num=0.5</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L86">[source]</a>
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

####Examples

```python
from hemlock import Debug as D, Input, Page, push_app_context
from hemlock.tools import chromedriver

app = push_app_context()

driver = chromedriver()

p = Page(Input(debug=D.send_keys('hello world')))
p.preview(driver)._debug(driver)
```

##hemlock.functions.debug.**random_str**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>random_str</b>(<i>driver, question, magnitude=2, p_whitespace=0.2</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L131">[source]</a>
</p>

Send a random string to the textarea.

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
<b>magnitude : <i>int, default=2</i></b>
<p class="attr">
    Maximum magnitude of the length of the string. e.g. the default magnitude of 2 means that the maximum length is 10^2=100 characters.
</p>
<b>p_whitespace : <i>float, default=.2</i></b>
<p class="attr">
    Frequency with which whitespace characters appear in the string.
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

p = Page(Input(debug=D.random_str()))
p.preview(driver)._debug(driver)
```

##hemlock.functions.debug.**random_number**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>random_number</b>(<i>driver, question, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L169">[source]</a>
</p>

Send a random number to the textarea or input.

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
<b>magn_lb : <i>int, default=0</i></b>
<p class="attr">
    Lower bound for the magnitude of the number.
</p>
<b>mag_ub : <i>int, default=10</i></b>
<p class="attr">
    Upper bound for the magnitude of the number.
</p>
<b>max_decimals : <i>int, default=5</i></b>
<p class="attr">
    Maximum number of decimals to which the number can be rounded.
</p>
<b>p_int : <i>float, default=.5</i></b>
<p class="attr">
    Probability that the number is an integer.
</p>
<b>p_neg : <i>float, default=.1</i></b>
<p class="attr">
    Probability that the number is negative.
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

p = Page(Input(debug=D.random_number()))
p.preview(driver)._debug(driver)
```

##hemlock.functions.debug.**send_datetime**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>send_datetime</b>(<i>driver, question, datetime_=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L212">[source]</a>
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

####Examples

```python
from hemlock import Debug as D, Input, Page, push_app_context
from hemlock.tools import chromedriver

from datetime import datetime

app = push_app_context()

driver = chromedriver()

p = Page(Input(input_type='date', debug=D.send_datetime(datetime.utcnow())))
p.preview(driver)._debug(driver)
```

##hemlock.functions.debug.**drag_range**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>drag_range</b>(<i>driver, range_, target=None, tol=0, max_iter=10</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L251">[source]</a>
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

####Examples

```python
from hemlock import Debug as D, Page, Range, push_app_context
from hemlock.tools import chromedriver

app = push_app_context()

driver = chromedriver()

p = Page(Range(debug=D.drag_range(80)))
p.preview(driver)._debug(driver)
```

##hemlock.functions.debug.**click_choices**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>click_choices</b>(<i>driver, question, *values</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L300">[source]</a>
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
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Check, Debug as D, Page, push_app_context
from hemlock.tools import chromedriver

app = push_app_context()

driver = chromedriver()

p = Page(
    Check(
        '<p>Click "Yes".</p>',
        ['Yes', 'No'],
        debug=D.click_choices('Yes')
    )
)
p.preview(driver)._debug(driver)
```

##hemlock.functions.debug.**clear_choices**

<p class="func-header">
    <i>def</i> hemlock.functions.debug.<b>clear_choices</b>(<i>driver, question</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/functions/debug.py#L352">[source]</a>
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
        '<p>Click "Yes".</p>',
        ['Yes', 'No'],
        multiple=True,
        debug=D.clear_choices()
    )
)
p.preview(driver)._debug(driver)
```