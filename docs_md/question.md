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
</style># Question mixins

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Question**

<p class="func-header">
    <i>class</i> hemlock.<b>Question</b>(<i>page=None, template='form-group.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/question.py#L17">[source]</a>
</p>

Base object for questions. Questions are displayed on their page in index order.

It inherits from `hemlock.Data` and `hemlock.HTMLMixin`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page or None, default=None</i></b>
<p class="attr">
    The page to which this question belongs.
</p>
<b>template : <i>str, default='form-group.html'</i></b>
<p class="attr">
    Template for the question <code>body</code>.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>default : <i>sqlalchemy_mutable.MutableType</i></b>
<p class="attr">
    Default question response.
</p>
<b>error : <i>str or None, default=None</i></b>
<p class="attr">
    Text of the question error message.
</p>
<b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Question label.
</p>
<b>response : <i>sqlalchemy_mutable.MutableType</i></b>
<p class="attr">
    Participant's response.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>part : <i>hemlock.Participant</i></b>
<p class="attr">
    The participant to which this question belongs. Derived from <code>self.page</code>.
</p>
<b>branch : <i>hemlock.Branch</i></b>
<p class="attr">
    The branch to which this question belongs. Derived from <code>self.page</code>.
</p>
<b>page : <i>hemlock.Page</i></b>
<p class="attr">
    The page to which this question belongs.
</p>
<b>compile_functions : <i>list of hemlock.Compile, default=[]</i></b>
<p class="attr">
    List of compile functions; run before the question is rendered.
</p>
<b>validate_functions : <i>list of hemlock.Validate, default=[]</i></b>
<p class="attr">
    List of validate functions; run to validate the participant's response.
</p>
<b>submit_functions : <i>list of hemlock.Submit, default=[]</i></b>
<p class="attr">
    List of submit functions; run after the participant's responses have been validated for all questions on a page.
</p>
<b>debug_functions : <i>list of hemlock.Debug, default=[]</i></b>
<p class="attr">
    List of debug functions; run during debugging. The default debug function is unique to the question type.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>clear_error</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/question.py#L152">[source]</a>
</p>

Clear the error message.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Question</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>clear_response</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/question.py#L163">[source]</a>
</p>

Clear the response.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Question</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**ChoiceQuestion**



A question which contains choices. Inherits from `hemlock.Question`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>multiple : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the participant can select multiple choices.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>choices : <i>list of hemlock.Choice, default=[]</i></b>
<p class="attr">
    Possible choices from which a participant can select.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>validate_choice</b>(<i>'choices') def validate_choice(self, key, val</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/question.py#L233">[source]</a>
</p>

Convert the assigned value if it is not alread a `Choice` object

This allows for the following syntax:
question.choices = ['Red','Green','Blue']

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

