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
</style># Choices and Options

The difference between `hemlock.Choice` and `hemlock.Option` is the former are
for `hemlock.Check` questions, while latter are for `hemlock.Select` questions.

The use of choice and option models is not due to any deep functional
difference between them, but reflects the underlying html.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Choice**

<p class="func-header">
    <i>class</i> hemlock.<b>Choice</b>(<i>label='', template='hemlock/choice.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models\choice.py#L17">[source]</a>
</p>

Choices are displayed as part of their question in index order.

It inherits from
[`hemlock.models.InputBase` and `hemlock.models.HTMLMixin`](bases.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str, default=''</i></b>
<p class="attr">
    Choice label.
</p>
<b>template : <i>str, default='choice.html'</i></b>
<p class="attr">
    Template for the choice <code>body</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>index : <i>int or None, default=None</i></b>
<p class="attr">
    Order in which this choice appears in its question.
</p>
<b>label : <i>str, default=''</i></b>
<p class="attr">
    The choice label.
</p>
<b>name : <i>str or None, default=None</i></b>
<p class="attr">
    Name of the choice column in the dataframe.
</p>
<b>value : <i>sqlalchemy_mutable.MutableType or None, default=None</i></b>
<p class="attr">
    Value of the data associated with the choice. For a question where only one choice can be selected, this is the value of the question's data if this choice is selected. For a question where multiple choices may be selected, data are one-hot encoded; the value is the suffix of the column name associated with the indicator variable that this choice was selected.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    The question to which this choice belongs.
</p></td>
</tr>
    </tbody>
</table>

####Notes

Passing `label` into the constructor is equivalent to calling
`self.set_all(label)` unless `name` and `value` arguments are also passed
to the constructor.

####Methods



<p class="func-header">
    <i></i> <b>set_all</b>(<i>self, val</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models\choice.py#L89">[source]</a>
</p>

Set the choice's label, name, and value.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>val : <i></i></b>
<p class="attr">
    Value to which the choice's label, name, and value should be set.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Choice</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>is_default</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models\choice.py#L105">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>is_default : <i>bool</i></b>
<p class="attr">
    Indicate that this choice is (one of) its question's default choice(s).
</p></td>
</tr>
    </tbody>
</table>

####Notes

The question's default choice(s) is the question's `response`, if not
`None`, or the question's `default`.

##hemlock.**Option**

<p class="func-header">
    <i>class</i> hemlock.<b>Option</b>(<i>label='', template='hemlock/option.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models\choice.py#L162">[source]</a>
</p>

Options are a choice polymorph for `hemlock.Select` questions.

Inherits from `hemlock.Choice`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str, default=''</i></b>
<p class="attr">
    Option label.
</p>
<b>template : <i>str, default='hemlock/option.html'</i></b>
<p class="attr">
    Template for the option <code>body</code>.
</p></td>
</tr>
    </tbody>
</table>



