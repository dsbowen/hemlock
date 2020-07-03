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
</style># Textarea

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**debug_func**

<p class="func-header">
    <i>def</i> hemlock.<b>debug_func</b>(<i>driver, question</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/textarea.py#L9">[source]</a>
</p>

Default debug function for textarea questions. See
[`random_keys`](debug_functions.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>question : <i>hemlock.Textarea</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**Textarea**

<p class="func-header">
    <i>class</i> hemlock.<b>Textarea</b>(<i>page=None, template='hemlock/textarea.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/textarea.py#L29">[source]</a>
</p>

Textareas provide large text boxes for free responses.

Inherits from [`hemlock.InputGroup`](input_group.md) and
[`hemlock.Question`](question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or bs4.BeautifulSoup, default=''</i></b>
<p class="attr">
    Textarea label.
</p>
<b>template : <i>str, default='hemlock/textarea.html'</i></b>
<p class="attr">
    Template for the textarea body.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>rows : <i>int, default=3</i></b>
<p class="attr">
    Number of rows of text to display.
</p>
<b>textarea : <i>bs4.Tag</i></b>
<p class="attr">
    The <code>&lt;textarea&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>

####Notes

Textareas have a default javascript which displays the number of words and
characters entered. This *cannot* be overridden by passing a `js` argument
to the constructor, although javascript can be modified after the
constructor has finished.

####Examples

```python
from hemlock import Page, Textarea, push_app_context

push_app_context()

p = Page([Textarea('<p>This is a textarea.</p>')])
p.preview() # p.preview('Ubuntu') if working in Ubuntu/WSL
```

####Methods



<p class="func-header">
    <i></i> <b>textarea_from_driver</b>(<i>self, driver</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/textarea.py#L90">[source]</a>
</p>

Get textarea from the webdriver for debugging.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    Selenium webdriver (does not need to be <code>Chrome</code>).
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>textarea : <i>selenium.webdriver.remote.webelement.WebElement</i></b>
<p class="attr">
    Web element of the <code>&lt;textarea&gt;</code> tag associated with this model.
</p></td>
</tr>
    </tbody>
</table>

