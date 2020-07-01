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
</style># Embedded data and timers

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Embedded**

<p class="func-header">
    <i>class</i> hemlock.<b>Embedded</b>(<i>parent=None, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/embedded.py#L9">[source]</a>
</p>

Embedded data belong to a branch or page. Use embedded data to manually
input data to the dataframe; as opposed to recording data from participant
responses.

Inherits from `hemlock.Data`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>parent : <i>hemlock.Branch, hemlock.Page, or None, default=None</i></b>
<p class="attr">
    The parent of this embedded data element.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>branch : <i>hemlock.Branch or None</i></b>
<p class="attr">
    The branch to which the embedded data element belongs.
</p>
<b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    The page to which this embedded data element belongs.
</p></td>
</tr>
    </tbody>
</table>





##hemlock.**Timer**



Tracks how much time a participant spends in various parts of the survey.

Inherits from `hemlock.Embedded`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>data : <i>float or None, default=None.</i></b>
<p class="attr">
    Read only. Number of seconds for which the timer has been running.
</p>
<b>end_time : <i>datetime.datetime or None, default=None</i></b>
<p class="attr">
    Read only. If the timer is running, this is the current time. If the timer is paused, this is the time at which the timer was last paused.
</p>
<b>start_time : <i>datetime.datetime or None, default=None</i></b>
<p class="attr">
    The time at which the timer was started.
</p>
<b>state : <i>str, default='not started'</i></b>
<p class="attr">
    <code>'not started'</code>, <code>'running</code>', or <code>'paused'</code>.
</p>
<b>total_time : <i>datetime.timedelta or None, default=None</i></b>
<p class="attr">
    Read only. Total time the timer has been running.
</p>
<b>unpause_time : <i>datetime.datetime or None, default=None</i></b>
<p class="attr">
    The time at which the timer was last unpaused.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>start</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/embedded.py#L100">[source]</a>
</p>

Start the timer.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Timer</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>pause</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/embedded.py#L116">[source]</a>
</p>

Pause the timer.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Timer</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>reset</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/embedded.py#L128">[source]</a>
</p>

Reset all attributes to their default values.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Timer</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

