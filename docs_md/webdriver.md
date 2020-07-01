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
</style># Selenium webdrivers

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**chromedriver**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>chromedriver</b>(<i>headless=False</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/webdriver.py#L8">[source]</a>
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