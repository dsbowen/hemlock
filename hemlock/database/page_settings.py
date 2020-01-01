"""Page settings

This file defines a `Page`'s default css and javascript, and compile, 
validate, and submit functions.
"""

from hemlock.app import Settings
from hemlock.tools import gen_external_css, gen_external_js, url_for

from bs4 import BeautifulSoup

def default_css():
    attrs_list = [
        {
            'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/css/bootstrap.min.css',
            'id': 'bootstrap-css'
        },
        {
            'href': '/hemlock/static/css/default.css',
            'id': 'hemlock-css'
        }
    ]
    css = BeautifulSoup('', 'html.parser')
    [css.append(gen_external_css(**attrs)) for attrs in attrs_list]
    return css

def default_js():
    attrs_list = [
        {
            'src': 'https://code.jquery.com/jquery-3.4.1.min.js',
            'id': 'jquery'
        },
        {
            'src': 'https://cdn.jsdelivr.net/npm/popper.js@1.16.0/dist/umd/popper.min.js',
            'id': 'popper'
        },
        {
            'src': 'https://stackpath.bootstrapcdn.com/bootstrap/4.4.1/js/bootstrap.min.js',
            'id': 'bootstrap-js'
        },
        {
            'src': '/hemlock/static/js/default.js',
            'id': 'hemlock-js'
        }
    ]
    js = BeautifulSoup('', 'html.parser')
    [js.append(gen_external_js(**attrs)) for attrs in attrs_list]
    return js

def compile_func(page):
    [q._compile() for q in page.questions]

def validate_func(page):
    [q._validate() for q in page.questions]
    
def submit_func(page):
    [q._submit() for q in page.questions]

@Settings.register('Page')
def page_settings():
    return {
        'css': default_css(),
        'js': default_js(),
        'back': False,
        'forward': True,
        'compile_functions': compile_func,
        'validate_functions': validate_func,
        'submit_functions': submit_func,
    }