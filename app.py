"""Hemlock application file"""

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