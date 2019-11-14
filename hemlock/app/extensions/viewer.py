"""Survey view"""

from hemlock.app.extensions.extensions_base import ExtensionsBase

from docx import Document
from docx.shared import Inches
from flask import Markup, current_app, render_template, send_file, url_for
from flask_download_btn import S3File
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
        self.s3_file = S3File(
            current_app.s3_client, 
            bucket=os.environ.get('BUCKET')
        )
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
        survey_view_file = SURVEY_VIEW_FILE.format(part.id)
        output = BytesIO()
        doc.save(output)
        import boto3
        s3 = boto3.resource(
            's3',
            aws_access_key_id=os.environ.get('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.environ.get('AWS_SECRET_ACCESS_KEY')
        )
        bucket = s3.Bucket(os.environ.get('BUCKET'))
        key = SURVEY_VIEW_FILE.format(part.id)
        bucket.put_object(output.getvalue(), Key=key)
        self.s3_file.key = key
        btn.downloads.append(self.s3_file.gen_download())
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