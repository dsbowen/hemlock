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
    status_p = Page(nav=researcher_navbar(), back=False, forward=False)
    status_p.js.append(current_app.socket_js)
    status_js = JS(filename='js/participants.js', blueprint='hemlock')
    status_p.js.append(status_js)
    status_txt = Text(status_p)
    Compile(status_txt, live_status)
    return status_p

def live_status(status_txt):
    """Set text to reflect participants' live status"""
    ds = DataStore.query.first()
    status_txt.text = PARTICIPANTS.format(**ds.current_status)