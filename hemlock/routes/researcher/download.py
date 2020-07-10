"""Data download"""

from ...app import bp, db
from ...models import Choice, Page, Participant, Option
from ...qpolymorphs import Check, CreateFile, Download, Input, Label, Select
from ...models.private import DataStore
from ...tools import chromedriver, join
from .login import researcher_login_required
from .utils import navbar, render, researcher_page

from bs4 import BeautifulSoup
from docx import Document
from docx.shared import Inches
from flask import request

import os
import re
from base64 import b64encode
from datetime import timedelta
from io import BytesIO
from itertools import chain
from zipfile import ZipFile

# Screen buffer for driver window height 
HEIGHT_BUFFER = 74
# Width of survey view for docx
SURVEY_VIEW_IMG_WIDTH = Inches(6)

SELECT_FILES_TXT = "<p>Select files to download.</p>"

SURVEY_VIEW_TXT = "<p>Enter participant IDs for survey viewing.</p>"

SURVEY_VIEW_PRESENTATION_TXT = "<p>Select presentation for viewing.</p>"

SURVEY_VIEW_FILE_TXT = "<p>Select the type of download.</p>"

INVALID_IDS = "<p>The following participant ID was invalid: {}.</p>"

"""1. Create a download page"""
@bp.route('/download', methods=['GET','POST'])
@researcher_login_required
def download():
    return render(download_page())

@researcher_page('download')
def download_page():
    """Return the Download page
    
    The download page allows researchers to select data download files and 
    survey view download files.
    """
    return Page(
        Check(
            SELECT_FILES_TXT, 
            [
                Choice('Data frame', value='data'),
                Choice('Participant metadata', value='meta')
            ], 
            multiple=True
        ),
        Input(
            SURVEY_VIEW_TXT, 
            validate_functions=valid_part_ids,
            submit_functions=record_part_ids,
        ),
        Select(
            SURVEY_VIEW_PRESENTATION_TXT,
            [
                Option('First presentation only', value='first'),
                Option('All presentations', value='all'),
            ],
        ),
        Select(
            SURVEY_VIEW_FILE_TXT,
            [
                Option('Screenshots', value='screenshot'),
                Option('Text', value='text'),
            ],
        ),
        Download(
            callback=request.url, 
            download_msg='Download complete',
            handle_form_functions=handle_download_form,
        ),
        navbar=navbar.render(), back=False, forward=False
    )

def valid_part_ids(survey_view_q):
    """
    Validate that requested participant IDs correspond to participants in 
    the database.

    Parameters
    ----------
    survey_view_q : hemlock.Input
        Input question where researchers input participant IDs.

    Returns
    -------
    error_msg : str or None
        A message displaying invalid participant IDs. If this message is 
        not `None`, the download will stop. Otherwise, it proceeds.
    """
    part_ids = re.split(r'\W+', survey_view_q.response)
    part_ids = [id for id in part_ids if id]
    invalid_ids = [i for i in part_ids if Participant.query.get(i) is None]
    if invalid_ids:
        return INVALID_IDS.format(join('and', *invalid_ids))

def record_part_ids(survey_view_q):
    """
    Record requested participant IDs in the data of the survey view question.

    Parameters
    ----------
    survey_view_q : hemlock.Input
    """
    part_ids = re.split(r'W+', survey_view_q.response)
    survey_view_q.data = [id for id in part_ids if id]

def handle_download_form(response, btn):
    """
    Adds the appropriate file creation function to the download button.

    Parameters
    ----------
    response : dict
        Form response; not used.

    btn : hemlock.Download
        Download button (last question on the download page).
    """
    download_p = download_page()
    db.session.add(download_p)
    btn.create_file_functions.clear()
    btn.downloads.clear()
    download_p._record_response()
    if download_p._validate():
        download_p._submit()
        # note: last question is the download button
        btn.create_file_functions = FileCreator(
            *(q.data for q in download_p.questions[:-1])
        )
    db.session.commit()


class FileCreator():
    """
    Creates the download zip file.

    Parameters
    ----------
    dataframes : dict
        Maps dataframe name (`'data'` or `'meta'`) to bool indicating that the
        researcher requested this dataframe.

    part_ids : list
        List of participant IDs requested for survey view.

    presentation : str
        Which page presentation to deliver for the survey view; first 
        presentation only or all presentations.

    download_type : str
        Type of download for the survey view; screenshot or text.

    Attributes
    ----------
    btn : hemlock.Download
    
    datastore : hemlock.models.DataStore

    driver : selenium.webdriver.chrome.webdriver.WebDriver
        Driver for taking screenshots for survey view.

    download_type : str
        Set from parameter.
    
    files : list of (filename, str [bytes]) tuples
        Requested download files.

    presentation : str
        Set from paramaeter.

    requested_dataframes : dict
        Set from `dataframes` parameter.

    requested_part : list of hemlock.Participant
        Participants whose survey view the researcher requested.
    """
    def __init__(self, dataframes, part_ids, presentation, download_type):
        self.btn = None
        self.datastore = None
        self.driver = None
        self.files = []

        self.requested_dataframes = dataframes
        self.requested_parts = Participant.query.filter(
            Participant.id.in_(part_ids)
        ).all()
        self.presentation = presentation
        self.download_type = download_type

    def __call__(self, btn):
        """
        Create and deliver the zip file with requested data files.

        Parameters
        ----------
        btn : hemlock.Download
        """
        # note: need to add requested participants before adding `to_store`
        # otherwise you get an error that you try to add the same participant
        # to the session multiple times.
        # I don't know why changing the order in which you add these lists
        # fixes the problem.
        db.session.add_all(self.requested_parts)
        self.btn = btn
        self.datastore = DataStore.query.first()
        db.session.add(self.datastore)
        if self.requested_dataframes.get('data'):
            for expr in self.prep_dataframe():
                yield expr
        if self.requested_dataframes.get('meta'):
            for expr in self.prep_meta():
                yield expr
        if self.requested_parts:
            for expr in self.gen_views():
                yield expr
        for expr in self.zip_files():
            yield expr

    def prep_dataframe(self):
        """
        Prepare the main data frame for download. Begin by storing data from
        participants whose data was updated since they were last stored in the
        data frame, or whose data has not yet been stored.
        """
        stage = 'Preparing data frame'
        yield self.btn.reset(stage, 0)
        parts = Participant.query.all()
        to_store = [
            p for p in parts 
            if p.updated or p not in self.datastore.parts_stored
        ]
        db.session.add_all(to_store)
        for i, part in enumerate(to_store):
            yield self.btn.report(stage, 100.*i/len(to_store))
            self.datastore.store_participant(part)
        self.files.append(self.datastore.data.get_download_file())
        yield self.btn.report(stage, 100)

    def prep_meta(self):
        """
        Prepare the participant metadata file.
        """
        stage = 'Preparing participant metadata'
        yield self.btn.reset(stage, 0)
        self.files.append(self.datastore.meta.get_download_file())
        yield self.btn.report(stage, 100)

    def gen_views(self):
        """
        Generate survey views for all requested participants.
        """
        if self.download_type == 'screenshot':
            self.driver = chromedriver(headless=True)
        generator = chain.from_iterable(
            (self.gen_view(part) for part in self.requested_parts)
        )
        for event in generator:
            yield event
        if self.driver is not None:
            self.driver.close()
            self.driver = None

    def gen_view(self, part):
        """
        Generate survey view for a single participant.

        Parameters
        ----------
        part : hemlock.Participant
        """
        stage = 'Creating survey view for participant '+str(part.id)
        yield self.btn.reset(stage, 0)
        doc = Document()
        if self.presentation == 'all':
            pages = part._viewing_pages
        elif self.presentation == 'first':
            pages = [p for p in part._viewing_pages if p.first_presentation]
        for i, page in enumerate(pages):
            yield self.btn.report(stage, 100.*i/len(pages))
            self.add_page_to_doc(doc, page)
        doc_bytes = BytesIO()
        doc.save(doc_bytes)
        self.files.append(('Participant-{}.docx'.format(part.id), doc_bytes))

    def add_page_to_doc(self, doc, page):
        """
        Add a viewing page to the document.

        Parameters
        ----------
        doc : docx.document.Document
            Survey view document for the current participant.

        page : hemlock.models.private.ViewingPage
            Page to add to the document.
        """
        if self.driver is None:
            text = BeautifulSoup(page.html, 'html.parser').text.strip('\n')
            doc.add_paragraph(text)
            return
        path = page.mkstmp()
        try:
            dist = os.environ.get('WSL_DISTRIBUTION')
            self.driver.get('file://'+('wsl$/'+dist+path if dist else path))
            self.accept_alerts()
            width = self.driver.get_window_size()['width']
            height = self.driver.execute_script(
                'return document.body.parentNode.scrollHeight'
            )
            self.driver.set_window_size(width, height+HEIGHT_BUFFER)
            form = self.driver.find_element_by_tag_name('form')
            page_bytes = BytesIO()
            page_bytes.write(form.screenshot_as_png)
            doc.add_picture(page_bytes, width=SURVEY_VIEW_IMG_WIDTH)
            page_bytes.close()
        except:
            pass
        os.remove(path)

    def accept_alerts(self):
        """
        Accept any alerts which may prevent the driver from loading the page 
        html.
        """
        try:
            while True:
                self.driver.switch_to.alert.accept()
        except:
            pass

    def zip_files(self):
        """
        Put all requested files in a zip archive and store in the download
        button's temporary downloads list.
        """
        stage = 'Zipping files'
        yield self.btn.reset(stage, 0)
        zipf_bytes = BytesIO()
        zipf = ZipFile(zipf_bytes, 'w')
        for i, (filename, io) in enumerate(self.files):
            yield self.btn.report(stage, 100.*i/len(self.files))
            zipf.writestr(filename, io.getvalue())
            io.close()
        zipf.close()
        data = b64encode(zipf_bytes.getvalue()).decode()
        url = 'data:application/zip;base64,' + data
        self.btn.tmp_downloads = [(url, 'hemlock-survey-data.zip')]
        zipf_bytes.close()
        yield self.btn.report(stage, 100)