"""Data Profile"""

from hemlock.routes.researcher.utils import *
from hemlock.routes.researcher.login import researcher_login_required

import pandas as pd
import pandas_profiling

from copy import copy
from datetime import timedelta

@bp.route('/profile')
@researcher_login_required
def profile():
    profile_p = profile_page()
    if not DataStore.query.first().data:
        profile_p.error = EMPTY_DATAFRAME
        return profile_p._render()
    return render_profile(profile_p)

@researcher_page('profile')
def profile_page():
    profile_p = Page(back=False, forward=False)
    Compile(profile_p, create_profile)
    CompileWorker(profile_p)
    return profile_p

def render_profile(profile_p):
    """Render the data profile

    Return the worker's loading page while the profile is being created. If 
    there is a error, return an error message. Otherwise, return the 
    rendered profile.

    Note that an error will occur if the researcher has not provisioned a 
    Redis server.
    """
    worker = profile_p.compile_worker
    try:
        if not worker.job_finished:
            return worker()
        worker.reset()
    except:
        profile_p.error = PROFILE_CREATION_ERR
        return profile_p._render()
    profile_report = profile_p.g.get('profile_report')
    if profile_report is None:
        profile_p.error = PROFILE_CREATION_ERR
        return profile_p._render()
    return profile_report.to_html()

def create_profile(profile_p):
    """Create the data profile"""
    df = pd.DataFrame(DataStore.query.first().data)
    if hasattr(current_app, 'clean_data') and current_app.clean_data:
        df = current_app.clean_data(df)
    try:
        profile_p.g = {'profile_report': df.profile_report()}
    except:
        pass