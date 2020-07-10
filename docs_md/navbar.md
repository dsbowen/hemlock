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
</style># Navigation bar

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

####Examples

```python
from hemlock import Page, push_app_context
from hemlock.tools import Navbar, Navitem, Navitemdd, Dropdownitem

app = push_app_context()

url_root = 'https://dsbowen.github.io/'

navbar = Navbar(
    'Hemlock',
    [
        Navitem('Application', href=url_root+'app'),
        Navitemdd(
            'Tools',
            [
                Dropdownitem('Language', href=url_root+'lang'),
                Dropdownitem('Navbar', href=url_root+'navbar')
           ]
        )
    ],
    href=url_root+'hemlock'
)

Page(navbar=navbar.render()).preview()
```

##hemlock.tools.**NavBase**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>NavBase</b>(<i>template, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L42">[source]</a>
</p>

All navigation models inherit from this base.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>template : <i>str</i></b>
<p class="attr">
    Path to template file. This is <em>not</em> a Jinja template, as you may wish to generate html for statics outside the application context.
</p>
<b>**kwargs : <i></i></b>
<p class="attr">
    Any attribute of navigation objects can be set by passing it as a keyword argument.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>a : <i>bs4.Tag</i></b>
<p class="attr">
    <code>&lt;a&gt;</code> tag.
</p>
<b>body : <i>bs4.BeautifulSoup (sqlalchemy_mutablesoup.MutableSoup)</i></b>
<p class="attr">
    Html container.
</p>
<b>label : <i>str</i></b>
<p class="attr">
    Navigation object label.
</p>
<b>href : <i>str</i></b>
<p class="attr">
    Hyperref associated with the object.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>is_active</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L97">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>is_active : <i>bool</i></b>
<p class="attr">
    Indicates that the object's href is active.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**Navbar**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Navbar</b>(<i>label='', navitems=[], template=os.path.join(DIR, 'navbar.html'), **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L110">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str, default=''</i></b>
<p class="attr">
    Navbar brand.
</p>
<b>navitems : <i>list of hemlock.tools.Navitem and hemlock.tools.Navitemdd</i></b>
<p class="attr">
    Navigation items associated with the navbar.
</p>
<b>template : <i>str, default='directory/navbar.html'</i></b>
<p class="attr">
    By default, this is a file stored in the directory of the current file.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>render</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L131">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>redered : <i>bs4.BeautifulSoup</i></b>
<p class="attr">
    A copy of <code>self.body</code> with rendered navitems.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**Navitem**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Navitem</b>(<i>label='', template=os.path.join(DIR, 'navitem.html'), ** kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L144">[source]</a>
</p>

Navigation item *without* dropdown items.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str, default=''</i></b>
<p class="attr">
    
</p>
<b>template : <i>str, default='directory/navitem.html'</i></b>
<p class="attr">
    By default, this is a file stored in the directory of the current file.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>render</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L162">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>rendered : <i>bs4.BeautifulSoup</i></b>
<p class="attr">
    Copy of <code>self.body</code>.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**Navitemdd**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Navitemdd</b>(<i>label='', dropdownitems=[], template=os.path.join(DIR, 'navitemdd.html'), **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L178">[source]</a>
</p>

Navigation item *with* dropdown items.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str, default=''</i></b>
<p class="attr">
    
</p>
<b>dropdownitems : <i>list of hemlock.tools.Dropdownitem</i></b>
<p class="attr">
    
</p>
<b>template : <i>str, default='directory/navitemdd.html'</i></b>
<p class="attr">
    By default, this is a file stored in the directory of the current file.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>render</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L199">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>rendered : <i>bs4.BeautifulSoup</i></b>
<p class="attr">
    A copy of <code>self.body</code> with rendered dropdown items.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**Dropdownitem**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Dropdownitem</b>(<i>label='', template=os.path.join(DIR, 'dropdownitem.html' ), **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L212">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str, default=''</i></b>
<p class="attr">
    
</p>
<b>template : <i>str, default='directory/dropdownitem.html'</i></b>
<p class="attr">
    By default, this is a file stored in the directory of the current file.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>render</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L228">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>rendered : <i>bs4.BeautifulSoup</i></b>
<p class="attr">
    Copy of <code>self.body</code>.
</p></td>
</tr>
    </tbody>
</table>

