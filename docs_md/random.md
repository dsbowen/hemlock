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
</style># Randomization tools

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.tools.**key**

<p class="func-header">
    <i>def</i> hemlock.tools.<b>key</b>(<i>len_=90</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/random.py#L12">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>len_ : <i>int, default=90</i></b>
<p class="attr">
    Length of the key to generate.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>key : <i>str</i></b>
<p class="attr">
    Randomly generated key of ascii letters and digits of specificed length.
</p></td>
</tr>
    </tbody>
</table>

####Notes

The first character is a letter. This allows you to use `key` to generate
strongly random id's for html elements. (Html element id's cannot start
with a digit.)

####Examples

```python
from hemlock import tools

tools.key(10)
```

Out:

```
gpGmZuRfF7
```

##hemlock.tools.**Randomizer**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Randomizer</b>(<i>elements, r=1, combination=True</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/random.py#L50">[source]</a>
</p>

Evenly randomizes over a set of elements.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>elements : <i>iterable</i></b>
<p class="attr">
    Set of elements over which to randomize.
</p>
<b>r : <i>int, default=1</i></b>
<p class="attr">
    Size of the subset of elements to select.
</p>
<b>combination : <i>bool, default=True</i></b>
<p class="attr">
    Indicates randomization over combinations of the elements, as opposed to permutations.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>elements : <i>iterable</i></b>
<p class="attr">
    Set from the <code>elements</code> parameter.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock.tools import Randomizer

elements = ('world','moon','star')
randomizer = Randomizer(elements, r=2, combination=False)
randomizer.next()
```

Out:

```
('moon', 'world')
```

####Methods



<p class="func-header">
    <i></i> <b>next</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/random.py#L95">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>subset : <i></i></b>
<p class="attr">
    Selected subset of elements.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.tools.**Assigner**

<p class="func-header">
    <i>class</i> hemlock.tools.<b>Assigner</b>(<i>conditions</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/random.py#L105">[source]</a>
</p>

Evenly assigns participants to conditions. Inherits from
`hemlock.tools.Randomizer`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>conditions : <i>dict</i></b>
<p class="attr">
    Maps condition variable name to iterable of possible assignments.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>keys : <i>iterable</i></b>
<p class="attr">
    Condition variable names.
</p>
<b>elements : <i>iterable</i></b>
<p class="attr">
    All possible combinations of condition values to which a participant may be assigned.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Participant, push_app_context
from hemlock.tools import Assigner

push_app_context()

part = Participant.gen_test_participant()
conditions = {'Treatment': (0,1), 'Level': ('low','med','high')}
assigner = Assigner(conditions)
assigner.next()
```

Out:

```
{'Treatment': 1, 'Level': 'low'}
```

In:

```python
[(e.var, e.data) for e in part.embedded]
```

Out:

```
[('Treatment', 0), ('Level', 'low')]
```

####Methods



<p class="func-header">
    <i></i> <b>next</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/tools/random.py#L160">[source]</a>
</p>

Assigns the participant to a condition. The condition assigment
updates the participant's metadata.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>assignment : <i>dict</i></b>
<p class="attr">
    Maps condition variable names to assigned conditions.
</p></td>
</tr>
    </tbody>
</table>

