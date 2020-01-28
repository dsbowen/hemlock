"""Utilities for researcher routes"""

from hemlock.app.factory import bp, db
from hemlock.database import *
from hemlock.database.private import DataStore
from hemlock.qpolymorphs import *
from hemlock.routes.researcher.texts import *
from hemlock.tools import *

from flask import current_app, redirect, request, session, url_for

PROFILE_SFX_LABELS = [
    ('overview', 'Overview'),
    ('variables', 'Variables'),
    ('correlations', 'Correlations'),
    ('missing', 'Missing Values'),
    ('sample', 'Sample')
]

BRAND = '''
<img src="/hemlock/static/img/hemlock_favicon.svg" class="d-inline-block align-top" alt="" style="max-height:30px;">
<span style="color:rgb(78,64,143);">Hemlock</span>
'''

def researcher_navbar():
    """Create a researcher navigation bar"""
    navbar = Navbar(label=BRAND, href='https://dsbowen.github.io/hemlock')
    navbar.a['target'] = '_blank'
    Navitem(navbar, label='Participant Status', href=url_for('hemlock.status'))
    Navitem(navbar, label='Download', href=url_for('hemlock.download'))
    navitem = Navitem(
        navbar, 
        label='Data Profile', 
        href=url_for('hemlock.profile')
    )
    navitem.a['target'] = '_blank'
    navitem.body.changed()
    Navitem(navbar, label='Logout', href=url_for('hemlock.logout'))
    return navbar

def researcher_page(key):
    """Decorator for retrieving or creating a researcher page

    The Flask session maps researcher page keys to IDs. This method attempts 
    to return a page whose ID is associated with the given session key. If 
    this page does not exist, it creates a page using create_page.
    """
    def wrapper(create_page):
        def get_or_create_page():
            if key in session:
                return Page.query.get(session[key])
            p = create_page()
            session_store(key, p.id)
            return p
        return get_or_create_page
    return wrapper

def session_store(key, val):
    """Store a key: value mapping in the session

    If the session is full, remove mappings from the session until space is 
    created to store the new mapping.
    """
    session[key] = val
    while key not in session:
        session.pop()
        session[key] = val

def render(page):
    """Compile, commit, and render a page"""
    worker = page.compile_worker
    if worker is not None:
        if not worker.job_finished:
            return worker()
        worker.reset()
    else:
        page._compile()
    html = page._render()
    db.session.commit()
    return html