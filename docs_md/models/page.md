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
</style># Page

The survey 'flow' is:

1. **Compile.** Execute a page's compile functions. By default, a page's
first compile function runs its questions' compile methods in index order.

2. **Render.** Render the page for the participant and wait for them to
respond.

3. **Record response.** Record the participant's response to every question on
the page. This sets the `response` attribute of the questions.

4. **Validate.** When the participant attempts to submit the page, validate
the responses. As with the compile method, the validate method executes a
page's validate functions in index order. By default, a page's first
validate function runs its questions' validate methods in index order.

5. **Record data.** Record the data associated with the participant's
responses to every question on the page. This sets the `data` attribute of the
questions.

6. **Submit.** Execute the page's submit functions. By default, a page's
first submit function runs its questions' submit methods in index order.

7. **Navigate.** If the page has a navigate function, create a new branch
originating from this page.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**compile_questions**

<p class="func-header">
    <i>def</i> hemlock.<b>compile_questions</b>(<i>page</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L53">[source]</a>
</p>

Execute the page's questions' compile methods in index order.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**validate_questions**

<p class="func-header">
    <i>def</i> hemlock.<b>validate_questions</b>(<i>page</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L64">[source]</a>
</p>

Execute the page's questions' validate methods in index order.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**submit_questions**

<p class="func-header">
    <i>def</i> hemlock.<b>submit_questions</b>(<i>page</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L75">[source]</a>
</p>

Execute the page's questions' submit methods in index order.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>page : <i>hemlock.Page</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**debug_questions**

<p class="func-header">
    <i>def</i> hemlock.<b>debug_questions</b>(<i>driver, page</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L86">[source]</a>
</p>

Execute the page's questions' debug methods in  *random* order.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>page : <i>hemlock.Page</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>



##hemlock.**navigate**

<p class="func-header">
    <i>def</i> hemlock.<b>navigate</b>(<i>driver, page, p_forward=0.8, p_back=0.1, sleep_time=3</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L101">[source]</a>
</p>

Randomly navigate forward or backward, or refresh the page. By default, it
is executed after the default page debug function.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver</i></b>
<p class="attr">
    
</p>
<b>page : <i>hemlock.Page</i></b>
<p class="attr">
    
</p>
<b>p_forward : <i>float, default=.8</i></b>
<p class="attr">
    Probability of clicking the forward button.
</p>
<b>p_back : <i>float, default=.1</i></b>
<p class="attr">
    Probability of clicking the back button.
</p>
<b>sleep_time : <i>float, default=3</i></b>
<p class="attr">
    Number of seconds to sleep if there is no forward or back button on the page.
</p></td>
</tr>
    </tbody>
</table>

####Notes

The probability of refreshing the page is `1-p_forward-p_back`.

##hemlock.**Page**

<p class="func-header">
    <i>class</i> hemlock.<b>Page</b>(<i>*questions, extra_css=[], extra_js=[], delay_forward= None, **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L185">[source]</a>
</p>

Pages are queued in a branch. A page contains a list of questions which it
displays to the participant in index order.

It inherits from [`hemlock.model.BranchingBase`](bases.md).

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>*questions : <i>list of hemlock.Question, default=[]</i></b>
<p class="attr">
    Questions to be displayed on this page.
</p>
<b>template : <i>str, default='hemlock/page-body.html'</i></b>
<p class="attr">
    Template for the page <code>body</code>.
</p>
<b>extra_css : <i>list, default=[]</i></b>
<p class="attr">
    List of extra css elements to add to the default css.
</p>
<b>extra_js : <i>list, default=[]</i></b>
<p class="attr">
    List of extra javascript elements to add to the default javascript.
</p>
<b>delay_forward : <i>int or None, default=None</i></b>
<p class="attr">
    Number of milliseconds for which to hide the forward button when the page is first displayed.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>back : <i>str or None, default=None</i></b>
<p class="attr">
    Text of the back button. If <code>None</code>, no back button will appear on the page. You may also set <code>back</code> to <code>True</code>, which will set the text to <code>'&lt;&lt;'</code>.
</p>
<b>back_btn_attrs : <i>dict or None, default=None</i></b>
<p class="attr">
    Dictionary of HTML attributes for the back button.
</p>
<b>banner : <i>str or None</i></b>
<p class="attr">
    Banner at the bottom of the page.
</p>
<b>cache_compile : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that this page should cache the result of its compile functions. Specifically, it removes all compile functions and the compile worker from the page self <code>self._compile</code> is called.
</p>
<b>css : <i>list</i></b>
<p class="attr">
    List of css elements.
</p>
<b>direction_from : <i>str or None, default=None</i></b>
<p class="attr">
    Direction in which the participant navigated from this page. Possible values are <code>'back'</code>, <code>'invalid'</code>, or <code>'forward'</code>.
</p>
<b>direction_to : <i>str or None, default=None</i></b>
<p class="attr">
    Direction in which the participant navigated to this page. Possible values are <code>'back'</code>, <code>'invalid'</code>, and <code>'forward'</code>.
</p>
<b>error : <i>str or None, default=None</i></b>
<p class="attr">
    Error message.
</p>
<b>error_attrs : <i>dict</i></b>
<p class="attr">
    Dicitonary of HTML attributes for the error alert.
</p>
<b>forward : <i>str or None, default='&gt;&gt;'</i></b>
<p class="attr">
    Text of the forward button. If <code>None</code>, no forward button will appear on the page. You may also set <code>forward</code> to <code>True</code>, which will set the text to <code>'&gt;&gt;'</code>.
</p>
<b>forward_btn_attrs : <i>dict</i></b>
<p class="attr">
    Dictionary of HTML attributes for the forward button.
</p>
<b>g : <i>misc, default=None</i></b>
<p class="attr">
    A miscellaneous object.
</p>
<b>index : <i>int or None, default=None</i></b>
<p class="attr">
    Order in which this page appears in its branch's page queue.
</p>
<b>js : <i>list</i></b>
<p class="attr">
    List of javascript elements.
</p>
<b>navbar : <i>str or None, default=None</i></b>
<p class="attr">
    Navigation bar.
</p>
<b>terminal : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the survey terminates on this page.
</p>
<b>viewed : <i>bool, default=False</i></b>
<p class="attr">
    Indicates that the participant has viewed this page.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Relationships:</b></td>
    <td class="field-body" width="100%"><b>part : <i>hemlock.Participant or None, default=None</i></b>
<p class="attr">
    Participant to which this page belongs. Read only; derived from <code>self. branch</code>.
</p>
<b>branch : <i>hemlock.Branch or None, default=None</i></b>
<p class="attr">
    Branch to which this page belongs.
</p>
<b>next_branch : <i>hemlock.Branch or None, default=None</i></b>
<p class="attr">
    Branch which originated from this page. This is automatically set when this page runs its navigate function.
</p>
<b>back_to : <i>hemlock.Page or None</i></b>
<p class="attr">
    Page to which this page navigates when going back. If <code>None</code>, this page navigates back to the previous page.
</p>
<b>forward_to : <i>hemlock.Page or None</i></b>
<p class="attr">
    Page to which this page navigates when going forward. If <code>None</code>, this page navigates to the next page.
</p>
<b>embedded : <i>list of hemlock.Embedded, default=[]</i></b>
<p class="attr">
    List of embedded data elements.
</p>
<b>timer : <i>hemlock.Timer or None, default=hemlock.Timer</i></b>
<p class="attr">
    Tracks timing data for this page. 1. Timer can be set as a <code>Timer</code> object. 2. Setting <code>timer</code> to a <code>str</code> or <code>None</code> sets the timer object variable. 3. Setting <code>timer</code> to a <code>tuple</code> sets the timer object variable and data rows. 4. Setting <code>timer</code> to a <code>dict</code> sets the timer object attributes. The <code>dict</code> maps attribute names to values.
</p>
<b>questions : <i>list of hemlock.Question, default=[]</i></b>
<p class="attr">
    List of questions which this page displays to its participant.
</p>
<b>data_elements : <i>list of hemlock.DataElement</i></b>
<p class="attr">
    List of data elements which belong to this page; in order, <code>self. timer</code>, <code>self.embedded</code>, <code>self.questions</code>.
</p>
<b>compile : <i>list of hemlock.Compile</i></b>
<p class="attr">
    List of compile functions; run before the page is rendered. The default page compile function runs its questions' compile functions in index order.
</p>
<b>compile_worker : <i>hemlock.Worker or None, default=None</i></b>
<p class="attr">
    Worker which sends the compile functions to a Redis queue.
</p>
<b>validate : <i>list of hemlock.Validate</i></b>
<p class="attr">
    List of validate functions; run to validate participant responses. The default page validate function runs its questions' validate functions in index order.
</p>
<b>validate_worker : <i>hemlock.Worker or None, default=None</i></b>
<p class="attr">
    Worker which sends the validate functions to a Redis queue.
</p>
<b>submit : <i>list of hemlock.Submit</i></b>
<p class="attr">
    List of submit functions; run after participant responses have been validated. The default submit function runs its questions' submit functions in index order.
</p>
<b>submit_worker : <i>hemlock.Worker or None, default=None</i></b>
<p class="attr">
    Worker which sends the submit functions to a Redis queue.
</p>
<b>navigate : <i>hemlock.Navigate or None, default=None</i></b>
<p class="attr">
    Navigate function which returns a new branch originating from this page.
</p>
<b>navigate_worker : <i>hemlock.Worker</i></b>
<p class="attr">
    Worker which sends the navigate function to a Redis queue.
</p>
<b>debug_functions : <i>list of hemlock.Debug</i></b>
<p class="attr">
    List of debug functions; run during debugging. The default debug function runs its questions' debug functions in <em>random</em> order.
</p></td>
</tr>
    </tbody>
</table>

####Notes

A CSS element can be any of the following:

1. Link tag (str) e.g., `'<link rel="stylesheet" href="https://my-css-url">'`
2. Href (str) e.g., `"https://my-css-url"`
3. Style dictionary (dict) e.g., `{'body': {'background': 'coral'}}`

The style dictionary maps a css selector to an attributes dictionary. The attributes dictionary maps attribute names to values.

A javascript element can be any of the following:

1. Attributes dictionary (dict) e.g., `{'src': 'https://my-js-url'}`
2. JS code (str)
3. Tuple of (attributes dictionary, js code)

####Examples

```python
from hemlock import Page, push_app_context

app = push_app_context()

Page(
    Label('Hello World')
).preview()
```

####Methods



<p class="func-header">
    <i></i> <b>clear_error</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L533">[source]</a>
</p>

Clear the error message from this page and all of its questions.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Page</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>clear_response</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L545">[source]</a>
</p>

Clear the response from all of this page's questions.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Page</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>convert_markdown</b>(<i>self, string, strip_last_paragraph=False</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L556">[source]</a>
</p>

Convert markdown-formatted string to HMTL.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>string : <i>str</i></b>
<p class="attr">
    Markdown-formatted string.
</p>
<b>strip_last_paragraph : <i>bool, default=False</i></b>
<p class="attr">
    Strips the <code>&lt;p&gt;</code> tag from the last paragraph. This often prettifies the display.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>HTML : <i>str</i></b>
<p class="attr">
    HTML-formatted string.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>first_page</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L575">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>is_first_page : <i>bool</i></b>
<p class="attr">
    Indicator that this is the first page in its participant's survey.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>last_page</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L590">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>is_last_page : <i>bool</i></b>
<p class="attr">
    Indicator that this is the last page in its participant's survey.
</p></td>
</tr>
    </tbody>
</table>

####Notes

This method assumes that if this page or its branch have a navigate
function or next branch that this page is not the last (i.e. that the
next branch will have pages). Avoid relying on this method if e.g.
this page's navigate function may return an empty branch.



<p class="func-header">
    <i></i> <b>is_valid</b>(<i>self</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L623">[source]</a>
</p>



<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>valid : <i>bool</i></b>
<p class="attr">
    Indicator that all of the participant's responses are valid. That is, that there are no error messages on the page or any of its questions.
</p></td>
</tr>
    </tbody>
</table>





<p class="func-header">
    <i></i> <b>preview</b>(<i>self, driver=None, dir='tmp', filename='preview', suffix= '.html', overwrite=False</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L634">[source]</a>
</p>

Preview the page in a browser window.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>driver : <i>selenium.webdriver.chrome.webdriver.WebDriver or None, default=None</i></b>
<p class="attr">
    Driver to preview page debugging. If <code>None</code>, the page will be opened in a web browser.
</p>
<b>dir : <i>str, default='tmp'</i></b>
<p class="attr">
    Directory to save the preview file. If the directory does not exist, this method creates it.
</p>
<b>filename : <i>str, default='preview'</i></b>
<p class="attr">
    Name of the preview file.
</p>
<b>suffix : <i>str, default='.html'</i></b>
<p class="attr">
    
</p>
<b>overwrite : <i>bool, default=False</i></b>
<p class="attr">
    Indicates to overwrite existing files of the same name.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>filepath : <i>str</i></b>
<p class="attr">
    Path to the preview file.
</p></td>
</tr>
    </tbody>
</table>

####Notes

This method does not run the compile functions.



<p class="func-header">
    <i></i> <b>view_nav</b>(<i>self, indent=0</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/models/page.py#L717">[source]</a>
</p>

Print the navigation starting at this page for debugging purposes.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>indent : <i>int, default=0</i></b>
<p class="attr">
    Starting indentation.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>self : <i>hemlock.Page</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

