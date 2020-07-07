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
</style># Branch

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Branch**

<p class="func-header">
    <i>class</i> hemlock.<b>Branch</b>(<i>*pages, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/branch.py#L9">[source]</a>
</p>

Branches are stacked in a participant's branch stack. A branch contains a
queue of pages which it displays to its participant.

Inherits from [`hemlock.models.Base`](bases.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>*pages : <i>hemlock.Page</i></b>
<p class="attr">
    Pages which belong to this branch.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>index : <i>int or None, default=None</i></b>
<p class="attr">
    Order in which this branch appears in its participant's branch stack.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>part : <i>hemlock.Participant</i></b>
<p class="attr">
    Participant to whose branch stack this page belongs.
</p>
<b>origin_branch : <i>hemlock.Branch</i></b>
<p class="attr">
    The branch from which this branch originated.
</p>
<b>next_branch : <i>hemlock.Branch</i></b>
<p class="attr">
    The branch which originated from this branch.
</p>
<b>origin_page : <i>hemlock.Page</i></b>
<p class="attr">
    The page from which this branch originated. Note that branches can originate from other branches or pages.
</p>
<b>pages : <i>list of hemlock.Page</i></b>
<p class="attr">
    The queue of pages belonging to this branch.
</p>
<b>start_page : <i>hemlock.Page or None</i></b>
<p class="attr">
    The first page in the page queue, if non-empty.
</p>
<b>current_page : <i>hemlock.Page</i></b>
<p class="attr">
    Current page of this branch (head of the page queue).
</p>
<b>embedded : <i>list of hemlock.Embedded</i></b>
<p class="attr">
    Embedded data elements.
</p>
<b>data_elements : <i>list of hemlock.DataElement</i></b>
<p class="attr">
    All data elements belonging to this branch, in order of embedded data then page data.
</p>
<b>navigate_function : <i>hemlock.Navigate</i></b>
<p class="attr">
    Navigate function which returns a new branch once the participant has reached the end of this branch (i.e. the end of the page queue associated with this branch).
</p>
<b>navigate_worker : <i>hemlock.NavigateWorker</i></b>
<p class="attr">
    Worker which handles complex navigate functions.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Branch, Label, Page, push_app_context

push_app_context()

b = Branch(
    Page(Label('<p>Hello World</p>')),
    Page(Label('<p>Hello Moon</p>')),
    Page(Label('<p>Hello Star</p>'))
)
b.preview() # b.preview('Ubuntu') if working in Ubuntu/WSL
```

This will open all of the branch's pages in separate tabs.

####Methods



<p class="func-header">
    <i></i> <b>view_nav</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/branch.py#L160">[source]</a>
</p>

Print this branch's page queue for debugging purposes.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Branch</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>preview</b>(<i>self, dist=None, driver=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/branch.py#L184">[source]</a>
</p>

Preview the page queue in the a browser window.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>dist : <i>str or None, default=None</i></b>
<p class="attr">
    Windows Subsystem for Linux (WSL) distribution (e.g. <code>'Ubuntu'</code>). Leave as <code>None</code> unless operating in WSL.
</p>
<b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver or None, default=None</i></b>
<p class="attr">
    Driver to preview page debugging. If <code>None</code>, the page will be opened in a web browser.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Branch</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

