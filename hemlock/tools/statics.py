"""Tool for generating statics"""

from bs4 import BeautifulSoup
from flask import render_template

__all__ = ['gen_external_css', 'gen_internal_css', 'gen_external_js']

def gen_soup(template, **attrs):
    soup = BeautifulSoup(template, 'html.parser')
    tag = list(soup.children)[0]
    [tag.__setitem__(key, val) for key, val in attrs.items()]
    return soup

def gen_external_css(**attrs):
    return gen_soup('<link rel="stylesheet" type="text/css"/>', **attrs)

def gen_internal_css(style):
    """Style maps css selectors to a dictionary of style attributes"""
    html = '<style></style>'
    soup = BeautifulSoup(html, 'html.parser')
    [
        soup.style.append(format_style(selector, attrs)) 
        for selector, attrs in style.items()
    ]
    return soup

def format_style(selector, attrs):
    attrs = ' '.join([attr+': '+val+';' for attr, val in attrs.items()])
    return selector+' {'+attrs+'}'

def gen_external_js(**attrs):
    return gen_soup('<script></script>', **attrs)