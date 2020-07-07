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
</style># Utilities

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**chromedriver**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>chromedriver</b>(<i>headless=False</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/utils.py#L9">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>headless : <i>bool, default=False</i></b>
<p class="attr">
    Indicates whether to run Chrome in headless mode.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Notes

Chromedriver must be headless in production. When the application is in
production, this method sets `headless` to `True` regardless of the
parameter you pass.

####Examples

```python
from hemlock.tools import chromedriver

driver = chromedriver()
```

##hemlock.tools.**get_data**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>get_data</b>(<i>dataframe='data'</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/utils.py#L47">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>dataframe : <i>str, default='data'</i></b>
<p class="attr">
    Name of the dataframe to get; <code>'data'</code> or <code>'meta'</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>data : <i>dict</i></b>
<p class="attr">
    Maps variable names to list of entries. May not include data from participants who are in progress.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Branch, Page, Participant, push_app_context
from hemlock.tools import get_data

def start():
    return Branch(Page())

push_app_context()

Participant.gen_test_participant(start).completed = True
get_data()
```

Out:

```
{'ID': [1],
'EndTime': [datetime.datetime(2020, 7, 6, 17, 11, 0, 245032)],
'StartTime': [datetime.datetime(2020, 7, 6, 17, 11, 0, 245032)],
'Status': ['Completed']}
```

##hemlock.tools.**url_for**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>url_for</b>(<i>*args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/utils.py#L87">[source]</a>
</p>

Attempt to return `flask.url_for(*args, **kwargs)`. However, this method
does not exit the program when getting a url outside a request context;
e.g. when debugging in a shell or notebook.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>*args, **kwargs : <i></i></b>
<p class="attr">
    Arguments and keyword arguments will be passed to <code>flask.url_for</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>url : <i>str</i></b>
<p class="attr">
    Output of <code>flask.url_for</code> if possible; otherwise <code>'URL_UNAVAILABLE'</code>.
</p></td>
</tr>
    </tbody>
</table>

