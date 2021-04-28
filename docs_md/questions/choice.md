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



##hemlock.**ChoiceBase**

<p class="func-header">
    <i>class</i> hemlock.<b>ChoiceBase</b>(<i>label=None, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L23">[source]</a>
</p>

Base class for choices.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Choice label.
</p>
<b>template : <i>str</i></b>
<p class="attr">
    Jinja template for the choice html.
</p>
<b>value : <i>default=None</i></b>
<p class="attr">
    Value of the choice if selected. e.g. a choice with label <code>'Yes'</code> might have a value of <code>1</code>. If <code>None</code>, the <code>label</code> is used. For a question where only one choice can be selected, this is the value of the question's data if this choice is selected. For a question where multiple choices may be selected, data are one-hot encoded; the value is the suffix of the column name associated with the indicator variable that this choice was selected.
</p>
<b>name : <i>default=None</i></b>
<p class="attr">
    Name associated with this choice in the dataframe. If <code>None</code>, the <code>label</code> is used.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>key : <i>str</i></b>
<p class="attr">
    Randomly generated from ascii letters and digits.
</p>
<b>label : <i>str</i></b>
<p class="attr">
    Set from the <code>label</code> parameter.
</p>
<b>value : <i></i></b>
<p class="attr">
    Set from the <code>value</code> parameter.
</p>
<b>name : <i></i></b>
<p class="attr">
    Set from the <code>name</code> parameter.
</p></td>
</tr>
    </tbody>
</table>

####Notes

If passing `value` and `name` to contructor, these must be passed as
keyword arguments

####Methods



<p class="func-header">
    <i></i> <b>is_default</b>(<i>self, question</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L75">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>question : <i>hemlock.Question</i></b>
<p class="attr">
    The question to which this choice belongs.
</p></td>
</tr>
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

The question's default choice(s) is the question's `response` if the
participant responded to the question, or the question's `default` if
the participant has not yet responded to the question.



<p class="func-header">
    <i></i> <b>set_all</b>(<i>self, val</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L104">[source]</a>
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
    <i></i> <b>dump</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L120">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>load</b>(<i>cls, state_dict</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L123">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**ChoiceListTypeBase**





<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>process_bind_param</b>(<i>self, choices, dialect</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L132">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>process_result_value</b>(<i>self, state_dicts, dialect</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L135">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**ChoiceListBase**



Converts items in a list of choices to the choice class.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>convert</b>(<i>cls, item</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L145">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Choice**

<p class="func-header">
    <i>class</i> hemlock.<b>Choice</b>(<i>label=None, template='hemlock/choice.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L172">[source]</a>
</p>

Choices are displayed as part of their question (usually
`hemlock.Check`). Inherits from `hemlock.ChoiceBase`.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Choice label.
</p>
<b>template : <i>str, default='hemlock/choice.html'</i></b>
<p class="attr">
    File name of the choice template.
</p>
<b>**kwargs : <i></i></b>
<p class="attr">
    Set the choice's value and name using keyword arguments.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>click</b>(<i>self, driver, if_selected=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L191">[source]</a>
</p>

Use a selenium webdriver to click on this choice.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    The selenium webdriver that clicks this choice. Does not have to be chromedriver.
</p>
<b>if_selected : <i>bool or None, default=None</i></b>
<p class="attr">
    Indicates that the choice will be clicked only if it is already selected. If <code>False</code> the choice will be clicked only if it is not already selected. If <code>None</code> the choice will be clicked whether or not it is selected.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>is_displayed</b>(<i>self, driver</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L220">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    The selenium webdriver that clicks this choice. Does not have to be chromedriver.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>is_displayed : <i>bool</i></b>
<p class="attr">
    Indicates that this choice is visible in the browser.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**ChoiceListType**





<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





##hemlock.**ChoiceList**





<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>







<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Option**

<p class="func-header">
    <i>class</i> hemlock.<b>Option</b>(<i>label=None, template='hemlock/option.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L257">[source]</a>
</p>

Options are displayed as part of their question (usually
`hemlock.Select`). Inherits from `hemlock.ChoiceBase`. Its functionality
is similar to `hemlock.Choice`, but for `Select` questions instead of
`Check` questions.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or None, default=None</i></b>
<p class="attr">
    Choice label.
</p>
<b>template : <i>str, default='hemlock/option.html'</i></b>
<p class="attr">
    File name of the option template.
</p>
<b>**kwargs : <i></i></b>
<p class="attr">
    Set the choice's value and name using keyword arguments.
</p></td>
</tr>
    </tbody>
</table>



####Methods



<p class="func-header">
    <i></i> <b>click</b>(<i>self, driver, if_selected=None</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L280">[source]</a>
</p>

Use a selenium webdriver to click on this choice.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    The selenium webdriver that clicks this choice. Does not have to be chromedriver.
</p>
<b>if_selected : <i>bool or None, default=None</i></b>
<p class="attr">
    Indicates that the choice will be clicked only if it is already selected. If <code>False</code> the choice will be clicked only if it is not already selected. If <code>None</code> the choice will be clicked whether or not it is selected.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i></i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>is_displayed</b>(<i>self, driver</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/choice.py#L308">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    The selenium webdriver that clicks this choice. Does not have to be chromedriver.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>is_displayed : <i>bool</i></b>
<p class="attr">
    Indicates that this choice is visible in the browser.
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**OptionListType**





<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>





##hemlock.**OptionList**





<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>







<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>

