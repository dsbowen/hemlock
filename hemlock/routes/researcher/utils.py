"""Utilities for researcher routes"""

from ...app import bp, db
from ...models import Page
from ...tools import Navbar, Navitem

from flask import current_app, redirect, request, session, url_for

LOGIN_REQUIRED = 'Login required to access this page.'

BRAND = '''
<img src="/hemlock/static/img/hemlock_favicon.svg" class="d-inline-block align-top" alt="" style="max-height:30px;">
<span style="font-family:'Josefin Sans';">HEMLOCK</span>
'''

navbar = Navbar(
    BRAND, 
    [
        Navitem('Participant status', href='/status'),
        Navitem('Download', href='/download'),
        # Navitem('Data profile', href='/profile'),
        Navitem('Logout', href='/logout'),
    ], 
    href='https://dsbowen.github.io/hemlock'
)
navbar.a['target'] = '_blank'
# navbar.navitems[-2].a['target'] = '_blank'

def researcher_page(key):
    """Decorator for retrieving or creating a researcher page

    The Flask session maps researcher page keys to IDs. This method attempts 
    to return a page whose ID is associated with the given session key. If 
    this page does not exist, it creates a page using create_page.
    """
    def wrapper(create_page):
        def get_or_create_page():
            try:
                return Page.query.get(session[key])
            except:
                pass
            p = create_page()
            session_store(key, p.id)
            return p
        return get_or_create_page
    return wrapper

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

def session_store(key, val):
    """Store a key: value mapping in the session

    If the session is full, remove mappings from the session until space is 
    created to store the new mapping.
    """
    session[key] = val
    while key not in session:
        session.pop()
        session[key] = val