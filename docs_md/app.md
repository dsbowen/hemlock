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
</style># Application factory and settings

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



##hemlock.app.**create_app**

<p class="func-header">
    <i>def</i> hemlock.app.<b>create_app</b>(<i>settings=settings</i>) <a class="src-href" target="_blank" href="https://github.com/dsbowen/hemlock/blob/master/hemlock/app/__init__.py#L40">[source]</a>
</p>

Create a Hemlock application.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>Parameters:</b></td>
    <td class="field-body" width="100%"><b>settings : <i>dict</i></b>
<p class="attr">
    Default settings for the application, extensions, and models.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Returns:</b></td>
    <td class="field-body" width="100%"><b>app : <i>flask.app.Flask</i></b>
<p class="attr">
    
</p></td>
</tr>
    </tbody>
</table>

####Examples

```python
from hemlock.app import create_app, settings

# MODIFY SETTINGS AS NEEDED

app = create_app(settings)
app.settings
```

Out:

```
{
    'clean_data': None,
    'restart_option': True,
    'restart_text': 'Click << to return to your in progress survey...'
    'screenout_keys': None,
    'screenout_text': '...you have already participated...',
    'socket_js_src': 'https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.3.0/socket.io.js',
    'time_expired_text': 'You have exceeded your time limit for this survey',
    'time_limit': None,
    'validate': True,
    'DownloadBtnManager': {},
    'Manager': {
        'loading_img_blueprint': 'hemlock',
        'loading_img_filename': 'img/worker_loading.gif'
    },
    'password_hash': '...'
}
```

## Default application settings

Below are the default settings for Hemlock applications and extensions.

<table class="docutils field-list field-table" frame="void" rules="none">
    <col class="field-name" />
    <col class="field-body" />
    <tbody valign="top">
        <tr class="field">
    <th class="field-name"><b>App settings:</b></td>
    <td class="field-body" width="100%"><b>clean_data : <i>callable or None, default=None</i></b>
<p class="attr">
    Callable which cleans your data before downloading or creating a data profile. This callable takes and returns <code>pandas.DataFrame</code>. If <code>None</code>, no additional cleaning is performend.
</p>
<b>password : <i>str, default=''</i></b>
<p class="attr">
    Password for accessing the researcher dashboard.
</p>
<b>restart_option : <i>bool, default=True</i></b>
<p class="attr">
    Indicates that participants who attempt to re-navigate to the index page will be given the option to restart the survey. If <code>False</code>, participants to attempt to re-navigate to the index page will be redirected to their current survey page.
</p>
<b>restart_text : <i>str, default='Click &lt;&lt; to return...'</i></b>
<p class="attr">
    Text displayed to participants when given the option to restart or continue with the survey.
</p>
<b>screenout_csv : <i>str or None, default=None</i></b>
<p class="attr">
    Name of the csv file containing criteria for screening out participants.
</p>
<b>screenout_text : <i>str, default='...you have already participated...'</i></b>
<p class="attr">
    Text displayed to participants who are ineligible to participate in this survey.
</p>
<b>socket_js_src : <i></i></b>
<p class="attr">
    Source of the websocket javascript.
</p>
<b>static_folder : <i>str, default='static'</i></b>
<p class="attr">
    Path to the static folder.
</p>
<b>template_folder : <i>str, default='templates'</i></b>
<p class="attr">
    Path to the template folder.
</p>
<b>time_expired_text : <i>str, default='You have exceeded your time limit...'</i></b>
<p class="attr">
    Text displayed to participants whose time has expired.
</p>
<b>time_limit : <i>datetime.timedelta or None, default=None</i></b>
<p class="attr">
    Time limit for participants to complete the survey.
</p>
<b>validate : <i>bool, default=True</i></b>
<p class="attr">
    Indicate that all validation is active. Set to <code>False</code> to turn off all validation for testing.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Config:</b></td>
    <td class="field-body" width="100%"><b>SECRET_KEY : <i>str</i></b>
<p class="attr">
    Looks for a <code>SECRET_KEY</code> environment variable.
</p>
<b>SQLALCHEMY_DATABASE_URI : <i>str</i></b>
<p class="attr">
    Looks for <code>DATABASE_URL</code> environment variable. Otherwise, we use a SQLite database <code>data.db</code>.
</p>
<b>SQLALCHEMY_TRACK_MODIFICATIONS : <i>bool, default=False</i></b>
<p class="attr">
    
</p>
<b>REDIS_URL : <i>str</i></b>
<p class="attr">
    Looks for a <code>REDIS_URL</code> environment variable.
</p></td>
</tr>
<tr class="field">
    <th class="field-name"><b>DownloadBtnManager:</b></td>
    <td class="field-body" width="100%"></td>
</tr>
<tr class="field">
    <th class="field-name"><b>Manager:</b></td>
    <td class="field-body" width="100%"><b>loading_img_blueprint : <i>str or None, default='hemlock'</i></b>
<p class="attr">
    Name of the blueprint to which the loading image belongs. If <code>None</code>, the loading image is assumed to be in the app's <code>static</code> directory.
</p>
<b>loading_img_filename : <i>str or None, default='img/worker_loading.gif'</i></b>
<p class="attr">
    Name of the loading image file.
</p></td>
</tr>
    </tbody>
</table>

####Notes

See <https://flask.palletsprojects.com/en/1.1.x/config/> for more detail on
Flask application configuration.

See <https://dsbowen.github.io/flask-download-btn/manager/> for more detail on
DownloadBtnManager settings.

See <https://dsbowen.github.io/flask-worker/manager/> for more detail on
Manager settings.