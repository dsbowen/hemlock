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
</style># Participant

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Participant**

<p class="func-header">
    <i>class</i> hemlock.<b>Participant</b>(<i>**kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/participant.py#L33">[source]</a>
</p>

The Participant class stores data for an individual survey participant and
handles navigation for that participant.

Inherits from [`hemlock.models.Base`](bases.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>completed : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the participant has completed the survey.
</p>
<b>end_time : <i>datetime.datetime</i></b>
<p class="attr">
    Last time the participant submitted a page.
</p>
<b>g : <i>dict, default={}</i></b>
<p class="attr">
    Dictionary of miscellaneous objects.
</p>
<b>meta : <i>dict, default={}</i></b>
<p class="attr">
    Participant metadata, such as IP address.
</p>
<b>start_time : <i>datetime.datetime</i></b>
<p class="attr">
    Time at which the participant started he survey.
</p>
<b>status : <i>str, default='InProgress'</i></b>
<p class="attr">
    Participant's current status; <code>'InProgress'</code>, <code>'TimedOut'</code>, or <code>'Completed'</code>. Read only; derived from <code>self.completed</code> and <code>self.time_expired</code>.
</p>
<b>time_expired : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the participant has exceeded their allotted time for the survey.
</p>
<b>updated : <i>bool, default=True</i></b>
<p class="attr">
    Indicates that the participant's data was updated after the last time their data was stored; if <code>True</code>, the participant's data will be re-stored when data are downloaded.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>branch_stack : <i>list of hemlock.Branch</i></b>
<p class="attr">
    The participant's stack of branches.
</p>
<b>current_branch : <i>hemlock.Branch</i></b>
<p class="attr">
    Participant's current branch (head of <code>self.branch_stack</code>).
</p>
<b>current_page : <i>hemlock.Page</i></b>
<p class="attr">
    Participant's current page (head of <code>self.current_branch</code>).
</p>
<b>pages : <i>list of hemlock.Page</i></b>
<p class="attr">
    Pages belonging to the participant.
</p>
<b>embedded : <i>list of hemlock.Embedded</i></b>
<p class="attr">
    Embedded data elements belonging to the participant.
</p>
<b>data_elements : <i>list of hemlock.DataElement</i></b>
<p class="attr">
    List of all data elements belonging to the participant, ordered by <code>id</code>.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock import Branch, Label, Page, Participant, push_app_context

def start():
    return Branch(Page(Label('<p>Hello World</p>')))

app = push_app_context()

part = Participant.gen_test_participant(start)
part.current_page.preview()
```

####Methods



<p class="func-header">
    <i></i> <b>back</b>(<i>self, back_to=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/participant.py#L227">[source]</a>
</p>

Navigate back for debugging purposes.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>back_to : <i>hemlock.Page or None, default=None</i></b>
<p class="attr">
    Navigate back to this page; if <code>None</code>, navigate back one page.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Participant</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>forward</b>(<i>self, forward_to=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/participant.py#L243">[source]</a>
</p>

Navigate forward for debugging purposes.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>forward_to : <i>hemlock.Page or None, default=None</i></b>
<p class="attr">
    Navigate forward to this page; if <code>None</code>, navigate forward one page.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Participant</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>gen_test_participant</b>(<i>gen_root=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/participant.py#L260">[source]</a>
</p>

Generate a test participant for debugging purposes.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>gen_root : <i>callable or None, default=None</i></b>
<p class="attr">
    Function to generate the root branch of the participant's tree. This should return a <code>hemlock.Branch</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>part : <i>hemlock.Participant</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>get_data</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/participant.py#L280">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>df : <i>hemlock.models.private.DataFrame</i></b>
<p class="attr">
    Data associated with the participant.
</p></td>
</tr>
    </tbody>
</table>

####Notes

Data elements are added to the dataframe in the order in which they
were created (i.e. by id). This is not necessarily the order in which
they appeared to the Participant.

####Examples





<p class="func-header">
    <i></i> <b>get_meta</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/participant.py#L345">[source]</a>
</p>

This is where it gets meta.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>meta : <i>dict</i></b>
<p class="attr">
    Participant's metadata, including the ID, end time, start time, and current status.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>view_nav</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/participant.py#L364">[source]</a>
</p>

View participant's branch stack.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Participant</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

