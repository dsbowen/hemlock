"""# Dashboard"""

from .. import tools
from ..app import db
from ..models import Question
from ..tools import iframe, key

from flask import render_template
from sqlalchemy_mutable import MutableDictType, MutableDictJSONType

import re
from urllib.parse import parse_qs, urlencode, urlparse


class Dashboard(Question):
    """
    Embeds a <a href="https://plotly.com/dash/" target="_blank">dash app</a>.

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Dashboard label.

    template : str, default='hemlock/dash.html'
        Template for the dashboard body.

    Attributes
    ----------
    src : str
        `src` attribute of the `<iframe>` tag.

    Examples
    --------
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
    \    return Branch(
    \        Page(
    \            Dashboard(src='/dashapp/', var='n_clicks')
    \        ),
    \        Page(
    \            Label('<p>The end.</p>'),
    \            terminal=True
    \        )
    \    )
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
    \    server=app,
    \    routes_pathname_prefix='/dashapp/',
    \    external_stylesheets=['https://codepen.io/chriddyp/pen/bWLwgP.css']
    )

    dash_app.layout = html.Div([
    \    dcc.Location(id='url'),
    \    html.Button('Click me!', id='button'),
    \    html.P(id='click-tracker'),
    ])

    @dash_app.callback(
    \    Output('click-tracker', 'children'),
    \    [Input('url', 'search'), Input('button', 'n_clicks')]
    )
    def update_clicks(search, n_clicks):
    \    n_clicks = n_clicks or 0
    \    Dashboard.record_response(search, n_clicks)
    \    return '{} clicks'.format(n_clicks)

    if __name__ == '__main__':
    \    from hemlock.app import socketio
    \    socketio.run(app, debug=True)
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
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'dashboard'}

    g = db.Column(MutableDictType)
    iframe_kwargs = db.Column(MutableDictJSONType)
    security_key = db.Column(db.String)

    _iframe_kwargs_keys = [
        'src', 'aspect_ratio', 'query_string', 'div_class', 'div_attrs',
        'iframe_class', 'iframe_attrs'
    ]

    def __init__(self, label=None, template='hemlock/dash.html', **kwargs):
        self.iframe_kwargs = {}
        self.security_key = key()
        super().__init__(label=label, template=template, **kwargs)

    def __getattribute__(self, key):
        if key == '_iframe_kwargs_keys' or key not in self._iframe_kwargs_keys:
            return super().__getattribute__(key)
        return self.iframe_kwargs.get(key)

    def __setattr__(self, key, val):
        if key in self._iframe_kwargs_keys:
            self.iframe_kwargs[key] = val
        else:
            super().__setattr__(key, val)

    @classmethod
    def get(cls, search):
        """
        Utility for retrieving a dashboard question in a dash callback.

        Parameters
        ----------
        search : str, formatted as URL query string
            Must have 'id' and 'key' parameters.

        Returns
        -------
        dashboard : hemlock_dash.Dashboard
            Dashboard specified by the id in the search string.

        Examples
        --------
        ```python
        ...
        import dash_core_components as dcc
        from hemlock import Dashboard

        app.layout = html.Div([
        \    dcc.Location(id='url', refresh=False),
        \    ...
        ])

        @app.callback(
        \    Output(...),
        \    [Input('url', 'search'), ...]
        )
        def my_callback(search, ...):
        \    dashboard = Dashboard.get(search)
        ```
        """
        qs = parse_qs(urlparse(search).query)
        id, key = qs['id'][0], qs['security_key'][0]
        dash = cls.query.get(id)
        return dash if dash.security_key == key else None

    @classmethod
    def record_response(cls, search, response):
        """
        Utility for writing the `response` attribute of the dashboard 
        question.

        Parameters
        ----------
        search : str, formatted as URL query string
            Must have 'id' and 'key' parameters.

        response : 
            Value to which to set the dash question's `repsonse` attribute.

        Returns
        -------
        dashboard : hemlock_dash.Dashboard
            Dashboard specified by the id in the search string.

        Examples
        --------
        ```python
        ...
        import dash_core_components as dcc
        from hemlock import Dashboard

        app.layout = html.Div([
        \    dcc.Location(id='url', refresh=False),
        \    ...
        ])

        @app.callback(
        \    Output(...),
        \    [Input('url', 'search'), ...]
        )
        def my_callback(search, ...):
        \    Dashboard.record_response(search, 'hello world')
        """
        dashboard = cls.get(search)
        dashboard.response = response
        db.session.commit()
        return dashboard

    def render_url(self):
        qs = self.iframe_kwargs.get('query_string', {}).copy()
        qs.update({'id': self.id, 'security_key': self.security_key})
        return self.src + '?' + urlencode(qs)

    def _render(self):
        # add id and security key to query string
        src = self.render_url()
        kwargs = {
            key: val for key, val in self.iframe_kwargs.items() 
            if key not in ('src', 'query_string')
        }
        return render_template(
            self.template, q=self, embed=iframe(src, **kwargs)
        )

    def _record_response(self):
        # response should be recorded in a callback
        return self