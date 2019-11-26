"""Data Profile"""

from hemlock.routes.researcher.utils import *
from hemlock.routes.researcher.login import researcher_login_required

from bs4 import BeautifulSoup
import pandas as pd
import pandas_profiling

@bp.route('/profile')
@researcher_login_required
def profile():
    return render(profile_page())

@researcher_page('profile')
def profile_page():
    profile_p = Page(nav=researcher_navbar(), back=False, forward=False)
    profile_txt = Text(profile_p)
    Compile(profile_txt, create_profile)
    return profile_p

def create_profile(profile_txt):
    data = DataStore.query.first().data
    if not data:
        profile_txt.page.error = 'No data currently available.'
        return
    profile_txt.page.error = None
    df = pd.DataFrame(DataStore.query.first().data)
    profile = df.profile_report(title='Data Profile')
    soup = BeautifulSoup(profile.to_html(), 'html.parser')
    profile_txt.css = [str(soup.find_all('style')[-1])]
    profile_txt.js = [str(soup.find_all('script')[-1])]
    profile_txt.text = convert_to_bootstrap4(profile.html)

def convert_to_bootstrap4(html):
    """Convert profile html from bootstrap 3 to 4"""
    soup = BeautifulSoup(html, 'html.parser')

    # label --> badge
    span_label_tags = soup.find_all('span', class_='label')
    for tag in span_label_tags:
        classes = tag.attrs['class']
        for i, class_ in enumerate(classes):
            classes[i] = class_.replace('label', 'badge')
        classes.append('badge-pill')
        tag.attrs['class'] = classes

    # add nav-item and nav-link class 
    nav_tab_tags = soup.find_all('ul', class_='nav nav-tabs')
    for tag in nav_tab_tags:
        items = tag.findChildren('li')
        for li in items:
            if 'class' not in li.attrs:
                li.attrs['class'] = []
            li.attrs['class'].append('nav-item')
            a = li.findChildren('a')[0]
            if 'class' not in a.attrs:
                a.attrs['class'] = []
            a.attrs['class'].append('nav-link')

    return str(soup)
    