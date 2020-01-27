"""Participant Status"""

from hemlock.routes.researcher.utils import *
from hemlock.routes.researcher.login import researcher_login_required

@bp.route('/status')
@researcher_login_required
def status():
    """View participants' live status"""
    return render(status_page())

@researcher_page('status')
def status_page():
    """Return the Participant Status page"""
    status_p = Page(navbar=researcher_navbar(), back=False, forward=False)
    status_p.add_external_js(src=current_app.socket_js_src)
    status_p.add_external_js(
        src=url_for('hemlock.static', filename='js/status.js')
    )
    status_label = Label(status_p)
    Compile(status_label, live_status)
    return status_p

def live_status(status_label):
    """Set text to reflect participants' live status"""
    ds = DataStore.query.first()
    status_label.label = PARTICIPANTS.format(**ds.current_status)