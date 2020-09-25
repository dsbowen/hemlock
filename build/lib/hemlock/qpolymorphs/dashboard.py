"""# Dashboard"""

from .. import tools
from ..app import db
from ..models import Question

import re
from urllib.parse import parse_qs, urlparse


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
    aspect_ratio : tuple of (int, int), default=(16, 9)
        Aspect ratio of the embedded application. See 
        <https://getbootstrap.com/docs/4.0/utilities/embed/#aspect-ratios>.

    embed : bs4.Tag
        `<div>` tag of the embedded app.

    iframe : bs4.Tag
        `<iframe>` tag of the embedded app.

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

    key = db.Column(db.String)

    def __init__(self, label='', template='hemlock/dash.html', **kwargs):
        super().__init__(label, template, **kwargs)

    @property
    def aspect_ratio(self):
        classes_ = self.embed['class']
        ratio_classes = [
            class_ for class_ in classes_ 
            if re.fullmatch('embed-responsive-\d+by\d+', class_)
        ]
        if not ratio_classes:
            return None, None
        ratio = ratio_classes[-1].strip('embed-responsive-').split('by')
        return int(ratio[0]), int(ratio[1])

    @aspect_ratio.setter
    def aspect_ratio(self, ratio):
        classes = self.embed['class']
        classes = [
            class_ for class_ in classes 
            if not re.fullmatch('embed-responsive-\d+by\d+', class_)
        ]
        classes.append('embed-responsive-{}by{}'.format(*ratio))
        self.embed['class'] = classes
        self.body.changed()

    @property
    def embed(self):
        return self.body.select_one('div.embed-responsive')

    @property
    def iframe(self):
        return self.body.select_one('iframe')
    
    @property
    def src(self):
        return self.iframe.attrs.get('src')

    @src.setter
    def src(self, val):
        self.iframe.attrs['src'] = val
        self.body.changed()

    @staticmethod
    def get(search):
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
        id, key = qs['id'][0], qs['key'][0]
        dash = Dashboard.query.get(id)
        return dash if dash.key == key else None

    @staticmethod
    def record_response(search, response):
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
        dashboard = Dashboard.get(search)
        dashboard.response = response
        db.session.commit()
        return dashboard

    def _render(self, body=None):
        self.key = tools.key()
        body = body or self.body.copy()
        iframe = body.select_one('iframe')
        # add id and key parameters to the src
        # these are used to get the dashboard object
        iframe['src'] += '?id='+str(self.id)+'&key='+self.key
        return super()._render(body)

    def _record_response(self):
        # response should be recorded in a callback
        return self