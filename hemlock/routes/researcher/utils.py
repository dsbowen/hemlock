"""Utilities for researcher routes"""
from ...tools import Navbar, Navitem, Navitemdd, Dropdownitem

navbar = Navbar(
    '''
    <img src="/hemlock/static/img/hemlock_favicon.svg" class="d-inline-block align-top" alt="" style="max-height:30px;">
    <span style="font-family:'Josefin Sans';">HEMLOCK</span>
    ''',
    href='https://dsbowen.github.io/hemlock',
    a_attrs={'target': '_blank'},
    navitems=[
        ('Participant status', '/status'),
        ('Download', '/download'),
        ('Logout', '/logout'),
    ]
)