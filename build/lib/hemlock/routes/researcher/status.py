"""Participant status"""

from ...app import bp
from ...models import Page
from ...models.private import DataStore
from ...qpolymorphs import Label
from .login import researcher_login_required
from .utils import navbar, render, researcher_page

from flask import current_app, url_for

PARTICIPANTS = """
<table align="center" style="width:50%">
    <tr>
        <th style="text-align:center" colspan="2">Participants' Current Status</th>
    </tr>
    <tr><td colspan="2"><hr/></td></tr>
    <tr>
        <td>Completed</td>
        <td id="Completed" align="right">{Completed}</td>
    </tr>
    <tr>
        <td>In Progress</td>
        <td id="InProgress" align="right">{InProgress}</td>
    </tr>
    <tr>
        <td>Timed Out</td>
        <td id="TimedOut" align="right">{TimedOut}</td>
    </tr>
    <tr>
        <td>Total</td>
        <td id="Total" align="right">{Total}</td>
    </tr>
</table>
"""

@bp.route('/status')
@researcher_login_required
def status():
    """View participants' live status"""
    return render(status_page())

@researcher_page('status')
def status_page():
    """Return the Participant Status page"""
    status_p = Page(Label(), navbar=navbar.render(), back=False, forward=False)
    status_p.add_external_js(src=current_app.settings['socket_js_src'])
    status_p.add_external_js(
        src=url_for('hemlock.static', filename='js/status.js')
    )
    status_p.questions[0].compile_functions = live_status
    return status_p

def live_status(status_label):
    """Set text to reflect participants' live status"""
    ds = DataStore.query.first()
    status_label.label = PARTICIPANTS.format(**ds.current_status)