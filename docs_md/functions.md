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
</style># Function models

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**FunctionRegistrar**



Mixin for Function models which provides a method for function registration.

Inherits from `sqlalchemy_function.FunctionMixin`. See
<https://dsbowen.github.io/sqlalchemy-function/>.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>register</b>(<i>self, func</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L29">[source]</a>
</p>

This decorator registers a function.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>func : <i>callable</i></b>
<p class="attr">
    The function to register.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**Compile**

<p class="func-header">
    <i>class</i> hemlock.<b>Compile</b>(<i>page=None, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L45">[source]</a>
</p>

Helps compile a page or question html before it is rendered and displayed to a participant.

Inherits from `hemlock.FunctionRegistrar`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>parent : <i>hemlock.Page, hemlock.Question, or None, default=None</i></b>
<p class="attr">
    The page or question to which this function belongs.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Set from the <code>parent</code> parameter.
</p>
<b>question : <i>hemlock.Question or None</i></b>
<p class="attr">
    Set from the <code>parent</code> parameter.
</p></td>
</tr>
    </tbody>
</table>





##hemlock.**Validate**

<p class="func-header">
    <i>class</i> hemlock.<b>Validate</b>(<i>parent=None, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L72">[source]</a>
</p>

Validates a participant's response.

Inherits from `hemlock.FunctionRegistrar`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>parent : <i>hemlock.Page, hemlock.Question, or None, default=None</i></b>
<p class="attr">
    The page or question to which this function belongs.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Set from the <code>parent</code> parameter.
</p>
<b>question : <i>hemlock.Question or None</i></b>
<p class="attr">
    Set from the <code>parent</code> parameter.
</p></td>
</tr>
    </tbody>
</table>





##hemlock.**Submit**

<p class="func-header">
    <i>class</i> hemlock.<b>Submit</b>(<i>parent=None, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L99">[source]</a>
</p>

Runs after a participant has successfully submitted a page.

Inherits from `hemlock.FunctionRegistrar`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>parent : <i>hemlock.Page, hemlock.Question, or None, default=None</i></b>
<p class="attr">
    The page or question to which this function belongs.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Set from the <code>parent</code> parameter.
</p>
<b>question : <i>hemlock.Question or None</i></b>
<p class="attr">
    Set from the <code>parent</code> parameter.
</p></td>
</tr>
    </tbody>
</table>





##hemlock.**Debug**

<p class="func-header">
    <i>class</i> hemlock.<b>Debug</b>(<i>parent=None, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L126">[source]</a>
</p>

Run to help debug the survey.

Inherits from `hemlock.FunctionRegistrar`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>parent : <i>hemlock.Page, hemlock.Question, or None, default=None</i></b>
<p class="attr">
    The page or question to which this function belongs.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    Set from the <code>parent</code> parameter.
</p>
<b>question : <i>hemlock.Question or None</i></b>
<p class="attr">
    Set from the <code>parent</code> parameter.
</p></td>
</tr>
    </tbody>
</table>





##hemlock.**Navigate**

<p class="func-header">
    <i>class</i> hemlock.<b>Navigate</b>(<i>parent=None, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L153">[source]</a>
</p>

Creates a new branch to which the participant will navigate.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>parent : <i>hemlock.Branch, hemlock.Page, or None, default=None</i></b>
<p class="attr">
    The branch or page to which this function belongs.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>branch : <i>hemlock.Branch</i></b>
<p class="attr">
    Set from the <code>parent</code> parameter.
</p>
<b>page : <i>hemlock.Page</i></b>
<p class="attr">
    Set from the <code>parent</code> parameter.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>__call__</b>(<i>self, *args, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/functions.py#L177">[source]</a>
</p>

Create a new branch and 'link' it to the tree. Linking in the new branch involves setting the `next_branch` and `origin_branch` or `origin_page` relationships.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

