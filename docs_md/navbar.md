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

See <https://dsbowen.github.io/sqlalchemy-nav>.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Navbar**



Navigation bar model.

Interits from `sqlalchemy_nav.NavbarMixin`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>pages : <i>list of hemlock.Page or None, default=None</i></b>
<p class="attr">
    Pages on which the navbar will be displayed.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>render</b>(<i>self, body=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/navbar.py#L26">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>body : <i>bs4.BeautifulSoup or None, default=None</i></b>
<p class="attr">
    Html body to render. If <code>None</code> render <code>self.body</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>html : <i>markupsafe.Markup</i></b>
<p class="attr">
    Rendered navbar for insertion into Jinja template.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**Navitem**



Item in the navigation bar.

Inherits from `sqlalchemy_nav.NavitemMixin`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





##hemlock.**Dropdownitem**



Dropdown item in a navigation item.

Inherits from `sqlalchemy_nav.DropdownitemMixin`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



