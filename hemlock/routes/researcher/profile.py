"""Data Profile"""

from hemlock.routes.researcher.utils import *
from hemlock.routes.researcher.login import researcher_login_required

from bs4 import BeautifulSoup
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
    download = Download(profile_p, text='Download Profile')
    CreateFile(download, store_profile)
    Text(profile_p)
    return profile_p

def create_profile(profile_p):
    """Create data profile and store in profile_txt question"""
    data = DataStore.query.first().data
    if not data:
        profile_p.error = 'No data currently available.'
        return
    profile_p.error = None
    download, profile_txt = profile_p.questions
    df = pd.DataFrame(DataStore.query.first().data)
    df = current_app.clean_data(df)
    profile = df.profile_report(title='Data Profile')
    html_full = profile.to_html()
    download.create_file_functions[0].args = [html_full]
    soup = BeautifulSoup(html_full, 'html.parser')
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
            if 'active' in li.attrs['class']:
                li.attrs['class'].remove('active')
                a.attrs['class'].append('active')

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