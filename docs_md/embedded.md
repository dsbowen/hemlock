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
    <i>class</i> hemlock.<b>Embedded</b>(<i>var=None, data=None, data_rows=1, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/embedded.py#L9">[source]</a>
</p>

Embedded data belong to a branch or page. Use embedded data to manually
input data to the dataframe; as opposed to recording data from participant
responses.

Polymorphic with [`hemlock.models.Data`](bases.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>var : <i>str or None, default=None</i></b>
<p class="attr">
    Variable name associated with this data element. If <code>None</code>, the data will not be recorded.
</p>
<b>data : <i>sqlalchemy_mutable.MutableType</i></b>
<p class="attr">
    Data this element contributes to the dataframe.
</p>
<b>data_rows : <i>int, default=1</i></b>
<p class="attr">
    Number of rows this data element contributes to the dataframe for its participant. If negative, this data element will 'fill in' any emtpy rows at the end of the dataframe with its most recent value.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>participant : <i>hemlock.Participant or None</i></b>
<p class="attr">
    The participant to whom this data element belongs.
</p>
<b>branch : <i>hemlock.Branch or None</i></b>
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

####Examples

```python
from hemlock import Branch, Embedded, Page, Participant, push_app_context

def start():
    return Branch(Page())

app = push_app_context()

part = Participant.gen_test_participant(start)
part.embedded = [Embedded('Name', 'Socrates', data_rows=-1)]
part.get_data()
```

Out:

```
{'ID': [1],
'EndTime': [datetime.datetime(2020, 7, 4, 17, 57, 23, 854272)],
'StartTime': [datetime.datetime(2020, 7, 4, 17, 57, 23, 854272)],
'Status': ['InProgress'],
'Name': ['Socrates'],
'NameOrder': [0],
'NameIndex': [0]}
```



##hemlock.**Timer**

<p class="func-header">
    <i>class</i> hemlock.<b>Timer</b>(<i>var=None, data_rows=1, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/embedded.py#L83">[source]</a>
</p>

Tracks how much time a participant spends in various parts of the survey.

Inherits from `hemlock.Embedded`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>data : <i>float or None</i></b>
<p class="attr">
    Read only. Number of seconds for which the timer has been running.
</p>
<b>end_time : <i>datetime.datetime or None</i></b>
<p class="attr">
    Read only. If the timer is running, this is the current time. If the timer is paused, this is the time at which the timer was last paused.
</p>
<b>start_time : <i>datetime.datetime or None</i></b>
<p class="attr">
    The time at which the timer was started.
</p>
<b>state : <i>str</i></b>
<p class="attr">
    <code>'not started'</code>, <code>'running</code>', or <code>'paused'</code>.
</p>
<b>total_time : <i>datetime.timedelta or None</i></b>
<p class="attr">
    Read only. Total time the timer has been running.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Timer, push_app_context

import time

app = push_app_context()

timer = Timer()
print(timer.state)
timer.start()
print(timer.state)
time.sleep(1)
print(timer.data)
timer.pause()
print(timer.state)
time.sleep(1)
print(timer.data)
```

Out:

```
not started
running
1.002405
paused
1.002983
```

####Methods



<p class="func-header">
    <i></i> <b>start</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/embedded.py#L172">[source]</a>
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
    <i></i> <b>pause</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/embedded.py#L188">[source]</a>
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
    <i></i> <b>reset</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/embedded.py#L200">[source]</a>
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

