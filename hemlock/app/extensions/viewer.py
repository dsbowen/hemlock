"""Survey view"""

from hemlock.app.extensions.extensions_base import ExtensionsBase

from docx import Document
from docx.shared import Inches
from flask import Markup, current_app, render_template, send_file, url_for
from itertools import chain
import imgkit
import os

STAGE = 'Creating Survey View for Participant {}'
SURVEY_VIEW_PATH = 'downloads/Participant-{}.docx'
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
        page_htmls = part._page_htmls.all()
        for i, page_html in enumerate(page_htmls):
            yield btn.report(stage, 100.0*i/len(page_htmls))
            print('finished report')
            self.store_page(doc, page_html)
            print('finished storing page (survey view)')
        survey_view_path = SURVEY_VIEW_PATH.format(part.id)
        print('about to save doc')
        doc.save(survey_view_path)
        print('doc saved')
        btn.filenames.append(survey_view_path)
        yield btn.report(stage, 100)   
        
    def store_page(self, doc, page_html):
        """Store a page in the survey view doc"""
        print('about to process page')
        page_html.process()
        print('page processed')
        page_name = 'downloads/Page-{}.png'.format(page_html.id)
        imgkit('hello world', page_name)
        # print('done storing token')
        # imgkit.from_string(
        #     page_html.html, page_name, css=page_html._css, 
        #     config=self.config, options=OPTIONS
        # )
        print('about to add picture to doc')
        doc.add_picture(page_name, width=SURVEY_VIEW_IMG_WIDTH)
        print('pic added to doc')
        os.remove(page_name)
        print('finished storing page (store page)')