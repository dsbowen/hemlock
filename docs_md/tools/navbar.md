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
        ('Application', href=url_root+'app'),
        (
            'Tools',
            [
                ('Language', href=url_root+'tools/lang'),
                ('Navbar', href=url_root+'tools/navbar')
           ]
        )
    ],
    href=url_root+'hemlock'
)

Page(navbar=navbar.render()).preview()
```

##hemlock.tools.**NavBase**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>NavBase</b>(<i>label, template, href='', a_class=[], a_attrs={}</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L43">[source]</a>
</p>

All navigation models inherit from this base.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters and attributes:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str</i></b>
<p class="attr">
    Label for the navigation element.
</p>
<b>template : <i>str</i></b>
<p class="attr">
    Path to template file or string. This is <em>not</em> a Jinja template, as you may wish to generate html for statics outside the application context.
</p>
<b>href : <i>str, default=''</i></b>
<p class="attr">
    Hyperref to which the navigation element links.
</p>
<b>a_attrs : <i>dict, default={}</i></b>
<p class="attr">
    Dictionary of HTML attributes for the navigation element's <code>&lt;a&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>render</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L82">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>rendered : <i>str</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**NavitemList**





<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>convert</b>(<i>cls, item</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L98">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**Navbar**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Navbar</b>(<i>label='', navitems=[], href='#', template=os.path.join( DIR, 'navbar.html'), a_class=['navbar-brand'], a_attrs={}, navbar_attrs ={'class': ['navbar', 'navbar-expand-lg', 'navbar-light', 'bg-light', 'fixed-top']}</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L111">[source]</a>
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
<b>navitems : <i>list of hemlock.tools.Navitem and hemlock.tools.Navitemdd</i></b>
<p class="attr">
    Navigation items associated with the navbar.
</p>
<b>href : <i>str, default=''</i></b>
<p class="attr">
    
</p>
<b>template : <i>str, default='directory/navbar.html'</i></b>
<p class="attr">
    By default, this is a file stored in the directory of the current file.
</p>
<b>a_attrs : <i>dict</i></b>
<p class="attr">
    
</p>
<b>navbar_attrs : <i>dict</i></b>
<p class="attr">
    HTML attributes for the <code>&lt;nav&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>render</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L157">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>rendered : <i>str</i></b>
<p class="attr">
    Rendered navbar HTML.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**Navitem**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Navitem</b>(<i>label='', href='', template=os.path.join(DIR, 'navitem.html'), a_class=['nav-item', 'nav-link'], a_attrs={}</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L172">[source]</a>
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
<b>href : <i>str, default=''</i></b>
<p class="attr">
    
</p>
<b>template : <i>str, default='directory/navitem.html'</i></b>
<p class="attr">
    By default, this is a file stored in the directory of the current file.
</p>
<b>a_attrs : <i>dict</i></b>
<p class="attr">
    
</p>
<b>navitem_attrs : <i>dict</i></b>
<p class="attr">
    HTML attributes for the <code>navitem</code> div.
</p></td>
</tr>
    </tbody>
</table>





##hemlock.tools.**DropdownitemList**





<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>convert</b>(<i>cls, item</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L200">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**Navitemdd**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Navitemdd</b>(<i>label='', dropdownitems=[], template=os.path.join(DIR, 'navitemdd.html'), a_class=['nav-item', 'nav-link', 'dropdown', 'dropdown-toggle'], a_attrs={'role': 'button', 'data-toggle': 'dropdown', 'aria-haspopup': 'true', 'aria-expanded': 'false'}, navitem_attrs={'class': ['nav-item', 'dropdown']}</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L210">[source]</a>
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
</p>
<b>a_attrs : <i>dict</i></b>
<p class="attr">
    
</p>
<b>navitem_attrs : <i>dict</i></b>
<p class="attr">
    HTML attributes for the <code>navitem</code> div.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>render</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L253">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>rendered : <i>str</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**Dropdownitem**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Dropdownitem</b>(<i>label='', href='', template=os.path.join(DIR, 'dropdownitem.html'), a_class=['dropdown-item'], a_attrs={}</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/navbar.py#L266">[source]</a>
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
<b>href : <i>str, default=''</i></b>
<p class="attr">
    
</p>
<b>template : <i>str, default='directory/dropdownitem.html'</i></b>
<p class="attr">
    By default, this is a file stored in the directory of the current file.
</p>
<b>a_attrs : <i>dict</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



