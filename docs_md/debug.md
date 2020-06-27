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
</style># Debugger

The debugger sends 'AI participants' through the survey. The AI
participants attempt to break the survey by clicking random objects and
entering random responses.

AI participants run in batches of specified sizes. For local debugging, I
recommend a batch size of 1. For production debugging, you can safely go up
to 3.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.debug.**debug**

<p class="func-header">
    <i>def</i> hemlock.debug.<b>debug</b>(<i>num_batches=1, batch_size=1</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/debug/__init__.py#L27">[source]</a>
</p>

Run the debugger.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>num_batches : <i>int, default=1</i></b>
<p class="attr">
    Number of batches of AI participants to run.
</p>
<b>batch_size : <i>int, default=1</i></b>
<p class="attr">
    Number of AI participants to run per batch.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>result : <i>bool</i></b>
<p class="attr">
    <code>True</code> if all AI participants in all batches run sucessfully. Otherwise, the program will crash.
</p></td>
</tr>
    </tbody>
</table>

####Notes

When called from the command line tool, `num_batches` and `batch_size` are
passed as strings.

##hemlock.debug.**run_batch**

<p class="func-header">
    <i>def</i> hemlock.debug.<b>run_batch</b>(<i>batch_size=1</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/debug/__init__.py#L53">[source]</a>
</p>

Run a batch of AI participants.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>batch_size : <i>int, default=1</i></b>
<p class="attr">
    Number of AI participants to run in this batch.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>result : <i>bool</i></b>
<p class="attr">
    <code>True</code> if all AI participants in this batch run successfully. Otherwise, the program will crash.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.debug.**run_participant**

<p class="func-header">
    <i>def</i> hemlock.debug.<b>run_participant</b>(<i></i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/debug/__init__.py#L78">[source]</a>
</p>

Run a single AI participant through the survey. Assert that the
participant does not encounter failures or errors.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>result : <i>bool</i></b>
<p class="attr">
    <code>True</code> if the participant ran successfully.
</p></td>
</tr>
    </tbody>
</table>

