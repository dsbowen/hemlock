"""Data Profile"""

from hemlock.routes.researcher.utils import *
from hemlock.routes.researcher.login import researcher_login_required

from bs4 import BeautifulSoup
from copy import copy
from datetime import timedelta
import pandas as pd
import pandas_profiling

@bp.route('/profile')
@researcher_login_required
def profile():
    return render(profile_page())

@researcher_page('profile')
def profile_page():
    profile_p = Page(nav=researcher_navbar(), back=False, forward=False)
    Compile(profile_p, create_profile)
    CompileWorker(profile_p)
    return profile_p

def create_profile(profile_p):
    """Create data profile and store in profile_txt question"""
    data = DataStore.query.first().data
    if not data:
        profile_p.error = 'No data currently available.'
        return
    profile_p.error = None
    html, inner_html = gen_profile_html()
    if not profile_p.questions:
        download = Download(profile_p, text='Download Profile')
        create_file_f = CreateFile(download, store_profile)
        profile_txt = Text(profile_p)
    else:
        download, profile_txt = profile_p.questions
        create_file_f = download.create_file_functions[0]
    create_file_f.args = [html]
    soup = BeautifulSoup(html, 'html.parser')
    css = str(soup.find_all('style')[-1])
    profile_txt.css = [to_bootstrap4_css(css)]
    profile_txt.js = [str(soup.find_all('script')[-1])]
    profile_txt.text = to_bootstrap4_html(inner_html)

def gen_profile_html():
    """Generate profile html page and inner html"""
    df = pd.DataFrame(DataStore.query.first().data)
    df = current_app.clean_data(df)
    profile = df.profile_report(check_recoded=False)
    return profile.to_html(), profile.html

def to_bootstrap4_css(css):
    return css.replace('.freq ', '')

def to_bootstrap4_html(inner_html):
    """Convert profile html from bootstrap 3 to 4"""
    soup = BeautifulSoup(inner_html, 'html.parser')

    # label --> badge
    span_label_tags = soup.select('span.label')
    for tag in span_label_tags:
        classes = tag.attrs['class']
        for i, class_ in enumerate(classes):
            classes[i] = class_.replace('label', 'badge')
        classes.append('badge-pill')
        tag.attrs['class'] = classes

    # add nav-item and nav-link class 
    nav_tab_tags = soup.select('ul.nav.nav-tabs')
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
            if 'active' in li.attrs['class']:
                li.attrs['class'].remove('active')
                a.attrs['class'].append('active')

    # show previews by default
    previews = soup.select('div.in.collapse')
    [p.attrs['class'].append('show') for p in previews]

    # figures and captions
    captions = soup.select('div.caption')
    for c in captions:
        c.name = 'figcaption'
        c_class = c.attrs['class']
        c_class.remove('caption')
        c_class.insert(0, 'figure-caption')
        c.parent.name = 'figure'
        parent_class = c.parent.attrs['class']
        parent_class.remove('row')
        parent_class.insert(0, 'figure')
        img_class = c.parent.findChildren('img')[0].attrs['class']
        img_class.insert(0, 'img-fluid')
        img_class.insert(0, 'figure-img')

    # frequency tables
    freq_tables = soup.select('table.freq')
    for table in freq_tables:
        table.attrs['class'].remove('freq')
        bars = table.select('div.bar')
        for bar in bars:
            bar.attrs['style'] += '; height:24px;'

    # toggle buttons
    btns = soup.select('a[role="button"]')
    for btn in btns:
        btn.attrs['href'] = '#'

    return str(soup)

def store_profile(btn, html):
    """Store data profile html page in bucket and download"""
    stage = 'Saving profile'
    yield btn.reset(stage, 0)
    bucket_filename = 'Profile-{}.html'.format(btn.id)
    blob = current_app.gcp_bucket.blob(bucket_filename)
    blob.upload_from_string(html)
    url = blob.generate_signed_url(expiration=timedelta(hours=1))
    btn.downloads = [(url, 'DataProfile.html')]
    yield btn.report(stage, 100)