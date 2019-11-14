"""Survey view"""

from hemlock.app.extensions.extensions_base import ExtensionsBase

from datetime import timedelta
from docx import Document
from docx.shared import Inches
from flask import Markup, current_app, render_template, send_file, url_for
from io import BytesIO
from itertools import chain
import imgkit
import os

STAGE = 'Creating Survey View for Participant {}'
SURVEY_VIEW_FILE = 'Participant-{}.docx'
SURVEY_VIEW_IMG_WIDTH = Inches(6)
OPTIONS = {'quiet':'', 'quality':100, 'zoom':1.5}


class Viewer(ExtensionsBase):
    def init_app(self, app):
        self._register_app(app, ext_name='viewer')
        wkhtmltoimage = app.config['WKHTMLTOIMAGE']
        self.config = imgkit.config(wkhtmltoimage=wkhtmltoimage)
    
    def survey_view(self, btn, parts):
        """Create a survey view for all participants (parts)"""
        gen_list = [self._survey_view(btn, part) for part in parts]
        return chain.from_iterable(gen_list)

    def _survey_view(self, btn, part):
        """Create survey view for a single participant (part)"""
        stage = STAGE.format(part.id)
        yield btn.reset(stage, 0)
        doc = Document()
        pages = part._viewing_pages.all()
        for i, page in enumerate(pages):
            yield btn.report(stage, 100.0*i/len(pages))
            self.store_page(btn, doc, page)
        self.store_doc(btn, doc, part.id)
        yield btn.report(stage, 100)
        
    def store_page(self, btn, doc, page):
        """Store a page in the survey view doc"""
        page.process()
        page_name = 'Page-{}.png'.format(page.id)
        imgkit.from_string(
            page.html, page_name, css=page.external_css_paths,
            config=self.config, options=OPTIONS
        )
        doc.add_picture(page_name, width=SURVEY_VIEW_IMG_WIDTH)
        os.remove(page_name)

    def store_doc(self, btn, doc, part_id):
        """Store documetn in GCP bucket"""
        filename = SURVEY_VIEW_FILE.format(part_id)
        output = BytesIO()
        doc.save(output)
        blob = current_app.gcp_bucket.blob(filename)
        blob.upload_from_string(output.getvalue())
        output.close()
        url = blob.generate_signed_url(expiration=timedelta(hours=1))
        btn.downloads.append((url, filename))