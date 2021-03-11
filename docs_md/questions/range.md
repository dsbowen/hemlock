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
</style># Range sliders

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**likert**

<p class="func-header">
    <i>def</i> hemlock.<b>likert</b>(<i>label=None, choices=5, default=0, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/range.py#L43">[source]</a>
</p>

Create a Likert slider.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str, default=None</i></b>
<p class="attr">
    
</p>
<b>choices : <i>int or list, default=5</i></b>
<p class="attr">
    A list of choices (str). May also be <code>5</code>, <code>7</code>, or <code>9</code> for default choice lists of length 5, 7, and 9. The list of choices should be an odd length and symmetric around the midpoint.
</p>
<b>default : <i>int, default=0</i></b>
<p class="attr">
    Default value. <code>0</code> is the scale midpoint.
</p>
<b>**kwargs : <i></i></b>
<p class="attr">
    Keyword arguments are passed to the <code>Slider</code> constructor.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>Likert : <i><code>Slider</code></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**Range**

<p class="func-header">
    <i>class</i> hemlock.<b>Range</b>(<i>label=None, template='hemlock/range.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/range.py#L97">[source]</a>
</p>

Range sliders can be dragged between minimum and maximum values in step
increments.

Inherits from [`hemlock.InputBase`](bases.md) and
[`hemlock.Question`](../models/question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Range label.
</p>
<b>template : <i>str, default='hemlock/range.html'</i></b>
<p class="attr">
    Template for the range body.
</p></td>
</tr>
    </tbody>
</table>

####Notes

Ranges have a default javascript which displays the value of the range
slider to participants. This will be appended to any `js` and `extra_js`
arguments passed to the constructor.

####Examples

```python
from hemlock import Range, Page, push_app_context

app = push_app_context()

Page(Range('This is a range slider.')).preview()
```



##hemlock.**RangeInput**

<p class="func-header">
    <i>class</i> hemlock.<b>RangeInput</b>(<i>label=None, template='hemlock/rangeinput.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/range.py#L145">[source]</a>
</p>

Range slider with an input field.

Inherits from [`hemlock.InputBase`](bases.md) and
[`hemlock.Question`](../models/question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Range label.
</p>
<b>template : <i>str, default='hemlock/rangeinput.html'</i></b>
<p class="attr">
    Template for the range body.
</p>
<b>width : <i>str, default='5em'</i></b>
<p class="attr">
    Width of the input field.
</p></td>
</tr>
    </tbody>
</table>

####Notes

Ranges have a default javascript which displays the value of the range
slider to participants. This will be appended to any `js` and `extra_js`
arguments passed to the constructor.

####Examples

```python
from hemlock import RangeInput, Page, push_app_context

app = push_app_context()

Page(RangeInput('This is a range slider.')).preview()
```



##hemlock.**Slider**

<p class="func-header">
    <i>class</i> hemlock.<b>Slider</b>(<i>label=None, template='hemlock/slider.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/range.py#L193">[source]</a>
</p>

Bootstrap slider.
<a href="https://github.com/seiyria/bootstrap-slider" target="_blank">See here</a>.

Inherits from [`hemlock.InputBase`](bases.md) and
[`hemlock.Question`](../models/question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Range label.
</p>
<b>template : <i>str, default='hemlock/slider.html'</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Notes

You can input the `formatter` parameter in one of three ways:

1. Javascript function (str). <a href="https://seiyria.com/bootstrap-slider/#example-1" target="_blank">See here</a>.
2. List of formatted values, one for each tick.
3. Dictionary mapping tick values to formatted values. Any ticks not mapped to a formatted value are displayed as the tick value.

####Examples

```python
from hemlock import Page, Slider, push_app_context

app = push_app_context()

Page(
    Slider(
        'This is a fancy Bootstrap slider',
        ticks=[0, 2, 4],
        ticks_labels=['very low', 'medium', 'high'],
        ticks_positions=[0, 50, 100],
        formatter=[
            'very low',
            'low',
            'medium',
            'high',
            'very high'
        ]
    )
).preview()
```

####Methods



<p class="func-header">
    <i></i> <b>get_max</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/range.py#L274">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>max : <i>scalar</i></b>
<p class="attr">
    Maximum value the slider can take.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>get_min</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/range.py#L285">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>min : <i>scalar</i></b>
<p class="attr">
    Minimum value the sldier can take.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>get_values</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/range.py#L296">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>values : <i>generator</i></b>
<p class="attr">
    Range of values the slider can take.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>get_midpoint</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/range.py#L306">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>midpoint : <i>scalar</i></b>
<p class="attr">
    Scale midpoint.
</p></td>
</tr>
    </tbody>
</table>

