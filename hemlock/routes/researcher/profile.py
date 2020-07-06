"""Data Profile"""

from ...app import bp
from ...models import Page, Worker
from ...models.private import DataStore
from .login import researcher_login_required
from .utils import navbar, render, researcher_page

import pandas as pd
import pandas_profiling
from flask import current_app

EMPTY_DATAFRAME = "No data are available to create the profle."

PROFILE_CREATION_ERR = '''
An error occurred while creating the data profile.<br/>
This may be because too few participants have completed the survey, or because you have not enabled background jobs.
'''

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
    return Worker.compile(Page(
        compile_functions=create_profile, back=False, forward=False, g={}
    ))

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
    if current_app.settings.get('clean_data'):
        df = current_app.clean_data(df)
    try:
        profile_p.g = {'profile_report': df.profile_report()}
    except:
        pass