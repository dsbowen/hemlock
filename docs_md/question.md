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
</style># Questions

`hemlock.Question` and `hemlock.ChoiceQuestion` are 'question skeletons';
most useful when fleshed out. See section on question polymorphs.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Question**

<p class="func-header">
    <i>class</i> hemlock.<b>Question</b>(<i>label='', template=None, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/question.py#L20">[source]</a>
</p>

Base object for questions. Questions are displayed on their page in index
order.

It inherits from
[`hemlock.models.Data` and `hemlock.models.HTMLMixin`](bases.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or bs4.BeautifulSoup, default=''</i></b>
<p class="attr">
    Question label.
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
    <td class="field-body" width="100%"><b>part : <i>hemlock.Participant or None</i></b>
<p class="attr">
    The participant to which this question belongs. Derived from <code>self.page</code>.
</p>
<b>branch : <i>hemlock.Branch or None</i></b>
<p class="attr">
    The branch to which this question belongs. Derived from <code>self.page</code>.
</p>
<b>page : <i>hemlock.Page or None</i></b>
<p class="attr">
    The page to which this question belongs.
</p>
<b>compile : <i>list of hemlock.Compile, default=[]</i></b>
<p class="attr">
    List of compile functions; run before the question is rendered.
</p>
<b>validate : <i>list of hemlock.Validate, default=[]</i></b>
<p class="attr">
    List of validate functions; run to validate the participant's response.
</p>
<b>submit : <i>list of hemlock.Submit, default=[]</i></b>
<p class="attr">
    List of submit functions; run after the participant's responses have been validated for all questions on a page.
</p>
<b>debug : <i>list of hemlock.Debug, default=[]</i></b>
<p class="attr">
    List of debug functions; run during debugging. The default debug function is unique to the question type.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>clear_error</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/question.py#L171">[source]</a>
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
    <i></i> <b>clear_response</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/question.py#L182">[source]</a>
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

<p class="func-header">
    <i>class</i> hemlock.<b>ChoiceQuestion</b>(<i>label='', choices=[], template=None, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/question.py#L235">[source]</a>
</p>

A question which contains choices. Inherits from `hemlock.Question`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or bs4.BeautifulSoup, default=''</i></b>
<p class="attr">
    Question label.
</p>
<b>choices : <i>list, default=[]</i></b>
<p class="attr">
    Choices which belong to this question. List items are usually <code>hemlock.Choice</code> or <code>hemlock.Option</code>.
</p>
<b>template : <i>str or None, default=None</i></b>
<p class="attr">
    Template for the question body.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>choices : <i>list, default=[]</i></b>
<p class="attr">
    Set from <code>choices</code> parameter.
</p>
<b>choice_cls : <i>class, default=hemlock.Choice</i></b>
<p class="attr">
    Class of the choices in the <code>choices</code> list.
</p>
<b>multiple : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the participant can select multiple choices.
</p></td>
</tr>
    </tbody>
</table>

####Notes

`choices` can be set using the following formats:
1. list of choice objects.
2. list of `str`, treated as choice labels.
3. list of `(choice label, value)` tuples.
4. list of `(choice label, value, name)` tuples.
5. list of dictionaries with choice keyword arguments.

