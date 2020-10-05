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
</style># Range slider

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Range**

<p class="func-header">
    <i>class</i> hemlock.<b>Range</b>(<i>label='', template='hemlock/range.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/range.py#L12">[source]</a>
</p>

Range sliders can be dragged between minimum and maximum values in step
increments.

Inherits from [`hemlock.InputBase`](bases.md) and
[`hemlock.Question`](question.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or bs4.BeautifulSoup, default=''</i></b>
<p class="attr">
    Range label.
</p>
<b>template : <i>str, default='hemlock/range.html'</i></b>
<p class="attr">
    Template for the range body.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>max : <i>float, default=100</i></b>
<p class="attr">
    Maximum value of the range slider.
</p>
<b>min : <i>float, default=0</i></b>
<p class="attr">
    Minimum value of the range slider.
</p>
<b>step : <i>float, default=1</i></b>
<p class="attr">
    Increments in which the range slider steps.
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

Page(Range('<p>This is a range slider.</p>')).preview()
```

