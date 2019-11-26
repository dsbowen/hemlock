"""Utilities for researcher routes"""

from hemlock.app.factory import bp, db
from hemlock.database import *
from hemlock.database.private import DataStore
from hemlock.question_polymorphs import *
from hemlock.routes.researcher.texts import *
from hemlock.tools import *

from flask import current_app, redirect, request, session, url_for

def researcher_navbar():
    """Return researcher navigation bar
    
    If the researcher navigation bar does not exist, create it.
    """
    navbar = Navbar.query.filter_by(name='researcher_navbar').first()
    if navbar is not None:
        return navbar
    navbar = Navbar(name='researcher_navbar')
    navbar.classes.append('fixed-top')
    Brand(bar=navbar, label='Hemlock')
    Navitem(
        bar=navbar, url=url_for('hemlock.status'), label='Participant Status'
    )
    Navitem(
        bar=navbar, url=url_for('hemlock.download'), label='Download'
    )
    profile_item = Navitem(
        bar=navbar, url=url_for('hemlock.profile'), label='Data Profile'
    )
    Dropdownitem(item=profile_item, url='#overview', label='Overview')
    Dropdownitem(item=profile_item, url='#variables', label='Variables')
    Dropdownitem(item=profile_item, url='#correlations', label='Correlations')
    Dropdownitem(item=profile_item, url='#missing', label='Missing Values')
    Dropdownitem(item=profile_item, url='#sample', label='Sample')
    Navitem(
        bar=navbar, url=url_for('hemlock.logout'), label='Logout'
    )
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
    page._compile()
    html = page._render()
    db.session.commit()
    return html