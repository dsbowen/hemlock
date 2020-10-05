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
</style># Common bases and mixins

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Base**

<p class="func-header">
    <i>class</i> hemlock.<b>Base</b>(<i>**kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/bases.py#L15">[source]</a>
</p>

Base for all Hemlock models.

Interits from
[`sqlalchemy_function.FunctionRelator`](https://dsbowen.github.io/sqlalchemy-function/),
[`sqlalchemy_orderingitem.Orderingitem`](https://dsbowen.github.io/sqlalchemy-orderingitem/) and
[`sqlalchemy_modelid.ModelIdBase`](https://dsbowen.github.io/sqlalchemy-modelid/).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>**kwargs : <i></i></b>
<p class="attr">
    You can set any attribute by passing it as a keyword argument.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>name : <i>str or None, default=None</i></b>
<p class="attr">
    Used primarily as a filter for database querying.
</p></td>
</tr>
    </tbody>
</table>





##hemlock.**Data**



Polymorphic base for all objects which contribute data to the dataframe.

Data elements 'pack' their data and return it to their participant, who in turn sends it to the data store.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>data : <i>sqlalchemy_mutable.MutableType, default=None</i></b>
<p class="attr">
    Data this element contributes to the dataframe.
</p>
<b>data_rows : <i>int, default=1</i></b>
<p class="attr">
    Number of rows this data element contributes to the dataframe for its participant. If negative, this data element will 'fill in' any emtpy rows at the end of the dataframe with its most recent value.
</p>
<b>index : <i>int or None, default=None</i></b>
<p class="attr">
    Order in which this data element appears in its parent; usually a <code>hemlock.Branch</code>, <code>hemlock.Page</code>, or <code>hemlock.Question</code>.
</p>
<b>var : <i>str or None, default=None</i></b>
<p class="attr">
    Variable name associated with this data element. If <code>None</code>, the data will not be recorded.
</p>
<b>record_order : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the order of this data element should be recorded in the datafame. The order is the order in which this element appeared relative to other elements with the same variable name.
</p>
<b>record_index : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the index of this data element should be recorded in the dataframe. The index is the order in which this element appeared relative to other elements with the same parent. For example, the index of a question is the order in which the question appeared on its page.
</p>
<b>record_choice_index : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the index of this data element's choices should be recorded in the dataframe. For example, a <code>hemlock.Check</code> question has multiple choices that the participant can select. The index of a choice is its index in the question's choice list.
</p></td>
</tr>
    </tbody>
</table>





##hemlock.**HTMLMixin**

<p class="func-header">
    <i>class</i> hemlock.<b>HTMLMixin</b>(<i>template=None, extra_css='', extra_js='', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/bases.py#L159">[source]</a>
</p>

Mixin for models which contribute html to a page.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>template : <i>str, default depends on object</i></b>
<p class="attr">
    Jinja template which is rendered to produce <code>self.body</code>.
</p>
<b>extra_css : <i>str or bs4.BeautifulSoup or list, default=''</i></b>
<p class="attr">
    Extra stylesheets to append to the default css.
</p>
<b>extra_js : <i>str or bs4.BeautifulSoup or list, default=''</i></b>
<p class="attr">
    Extra scripts to append to the default javascript.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>attrs : <i>dict</i></b>
<p class="attr">
    Most objects subclassing the <code>HTMLMixin</code> have a dictionary or html attributes for the main html tag of the <code>body</code>. For example, the <code>Input</code> object's main tag is an <code>&lt;input&gt;</code> tag with attributes such as <code>type</code>, <code>min</code>, and <code>max</code>.
</p>
<b>body : <i>sqlalchemy_mutablesoup.MutableSoupType</i></b>
<p class="attr">
    The main html of the object.
</p>
<b>css : <i>sqlalchemy_mutablesoup.MutableSoupType, default=''</i></b>
<p class="attr">
    CSS the object contributes to the page.
</p>
<b>js : <i>sqlalchemy_mutablesoup.MutableSoupType, default=''</i></b>
<p class="attr">
    Javascript the object contributes to the page.
</p></td>
</tr>
    </tbody>
</table>

####Notes

`HTMLMixin` also allows you to set attributes of the main html tag as if
setting an attribute of the `HTMLMixin` object. For example, you can set
the `type` of the `<input>` tag of an `hemlock.Input` question with:

```python
from hemlock import Input, push_app_context

app = push_app_context()

inpt = Input(type='number')
inpt.body
```

Out:

```
...
<input class="form-control" id="input-1" name="input-1" type="number"/>
...
```

Valid html attributes will vary depending on the object.

####Methods



<p class="func-header">
    <i></i> <b>add_external_css</b>(<i>self, **attrs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/bases.py#L267">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>**attrs : <i></i></b>
<p class="attr">
    Attribute names and values in the <code>&lt;link/&gt;</code> tag.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.HTMLMiixn</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Notes

See (statics.md#hemlocktoolsexternal_css).



<p class="func-header">
    <i></i> <b>add_internal_css</b>(<i>self, style</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/bases.py#L287">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>style : <i>dict</i></b>
<p class="attr">
    Maps css selector to an attributes dictionary. The attributes dictionary maps attribute names to values.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.HTMLMixin</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Notes

See (statics.md#hemlocktoolsinternal_css).



<p class="func-header">
    <i></i> <b>add_external_js</b>(<i>self, **attrs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/bases.py#L308">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>**attrs : <i></i></b>
<p class="attr">
    Attribute names and values in the <code>&lt;script&gt;</code> tag.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.HTMLMixin</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Notes

See (statics.md#hemlocktoolsexternal_js).



<p class="func-header">
    <i></i> <b>add_internal_js</b>(<i>self, js</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/bases.py#L328">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>js : <i>str</i></b>
<p class="attr">
    Javascript code.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.HTMLMixin</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Notes

See (statics.md#hemlocktoolsinternal_js).



<p class="func-header">
    <i></i> <b>update_attrs</b>(<i>self, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/bases.py#L348">[source]</a>
</p>

Update html tag attributes.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>**kwargs : <i></i></b>
<p class="attr">
    Keyword arguments map attribute names to values.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**InputBase**



Base for models which contain `<input>` tags.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>attrs : <i>dict</i></b>
<p class="attr">
    Input tag html attributes.
</p>
<b>input : <i>bs4.Tag or None</i></b>
<p class="attr">
    Input tag associated with this model.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>input_from_driver</b>(<i>self, driver=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/bases.py#L424">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.Webdriver</i></b>
<p class="attr">
    Driver which will be used to select the input. Does not need to be Chrome.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>input : <i>selenium.webdriver.remote.webelement.WebElement</i></b>
<p class="attr">
    Web element of the <code>&lt;input&gt;</code> tag associated with this model.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>label_from_driver</b>(<i>self, driver</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/bases.py#L438">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.Webdriver</i></b>
<p class="attr">
    Driver which will be used to select the label. Does not need to be Chrome.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>label : <i>selenium.webdriver.remote.webelement.WebElement</i></b>
<p class="attr">
    Web element of the label tag associated with this model.
</p></td>
</tr>
    </tbody>
</table>

