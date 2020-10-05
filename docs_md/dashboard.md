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
</style># Dashboard

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        
    </tbody>
</table>



##hemlock.**Dashboard**

<p class="func-header">
    <i>class</i> hemlock.<b>Dashboard</b>(<i>label='', template='hemlock/dash.html', **kwargs</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/dashboard.py#L13">[source]</a>
</p>

Embeds a <a href="https://plotly.com/dash/" target="_blank">dash app</a>.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>label : <i>str or bs4.BeautifulSoup, default=''</i></b>
<p class="attr">
    Dashboard label.
</p>
<b>template : <i>str, default='hemlock/dash.html'</i></b>
<p class="attr">
    Template for the dashboard body.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Attributes:</b></td>
    <td class="field-body" width="100%"><b>aspect_ratio : <i>tuple of (int, int), default=(16, 9)</i></b>
<p class="attr">
    Aspect ratio of the embedded application. See <a href="https://getbootstrap.com/docs/4.0/utilities/embed/#aspect-ratios">https://getbootstrap.com/docs/4.0/utilities/embed/#aspect-ratios</a>.
</p>
<b>embed : <i>bs4.Tag</i></b>
<p class="attr">
    <code>&lt;div&gt;</code> tag of the embedded app.
</p>
<b>g : <i>dict</i></b>
<p class="attr">
    <a href="https://dsbowen.github.io/sqlalchemy-mutable/">Mutable dictionary</a> with dashboard arguments.
</p>
<b>iframe : <i>bs4.Tag</i></b>
<p class="attr">
    <code>&lt;iframe&gt;</code> tag of the embedded app.
</p>
<b>src : <i>str</i></b>
<p class="attr">
    <code>src</code> attribute of the <code>&lt;iframe&gt;</code> tag.
</p></td>
</tr>
    </tbody>
</table>

####Examples

In this example, we create a simple dash app in which participants click on a
button. We embed this app in a hemlock survey, and record the number of times
a participant clicked the button.

Install `dash` with:

```bash
$ hlk install dash
```

Or:

```bash
$ pip install dash
```

In `survey.py`:

```python
from hemlock import Branch, Dashboard, Label, Page, route

@route('/survey')
def start():
    return Branch(
        Page(
            Dashboard(src='/dashapp/', var='n_clicks')
        ),
        Page(
            Label('<p>The end.</p>'),
            terminal=True
        )
    )
```

In `app.py`:

```python
import survey

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from hemlock import Dashboard, create_app

app = create_app()
dash_app = dash.Dash(
    server=app,
    routes_pathname_prefix='/dashapp/',
    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
)

dash_app.layout = html.Div([
    dcc.Location(id='url'),
    html.Button('Click me!', id='button'),
    html.P(id='click-tracker'),
])

@dash_app.callback(
    Output('click-tracker', 'children'),
    [Input('url', 'search'), Input('button', 'n_clicks')]
)
def update_clicks(search, n_clicks):
    n_clicks = n_clicks or 0
    Dashboard.record_response(search, n_clicks)
    return '{} clicks'.format(n_clicks)

if __name__ == '__main__':
    from hemlock.app import socketio
    socketio.run(app, debug=True)
```

Run the app with:

```bash
$ hlk serve
```

Or:

```bash
$ python app.py
```

Then open your browser and navigate to <http://localhost:5000/>.

####Methods



<p class="func-header">
    <i></i> <b>get</b>(<i>search</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/dashboard.py#L181">[source]</a>
</p>

Utility for retrieving a dashboard question in a dash callback.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>search : <i>str, formatted as URL query string</i></b>
<p class="attr">
    Must have 'id' and 'key' parameters.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>dashboard : <i>hemlock_dash.Dashboard</i></b>
<p class="attr">
    Dashboard specified by the id in the search string.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
...
import dash_core_components as dcc
from hemlock import Dashboard

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    ...
])

@app.callback(
    Output(...),
    [Input('url', 'search'), ...]
)
def my_callback(search, ...):
    dashboard = Dashboard.get(search)
```



<p class="func-header">
    <i></i> <b>record_response</b>(<i>search, response</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/qpolymorphs/dashboard.py#L221">[source]</a>
</p>

Utility for writing the `response` attribute of the dashboard
question.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>search : <i>str, formatted as URL query string</i></b>
<p class="attr">
    Must have 'id' and 'key' parameters.
</p>
<b>response : <i></i></b>
<p class="attr">
    Value to which to set the dash question's <code>repsonse</code> attribute.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>dashboard : <i>hemlock_dash.Dashboard</i></b>
<p class="attr">
    Dashboard specified by the id in the search string.
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
...
import dash_core_components as dcc
from hemlock import Dashboard

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    ...
])

@app.callback(
    Output(...),
    [Input('url', 'search'), ...]
)
def my_callback(search, ...):
    Dashboard.record_response(search, 'hello world')