##############################################################################
# Survey viewer class
# by Dillon Bowen
# last modified 08/17/2019
##############################################################################

import os
import imgkit
import zipfile
from hemlock.extensions.extensions_base import ExtensionsBase
from flask import url_for, render_template, Markup, send_file
from docx import Document
from docx.shared import Inches

SURVEY_VIEW_ZIP = 'survey_view.zip'
SURVEY_VIEW_DOC = 'survey_view.docx'
TMPDIR = 'tmp'
SURVEY_VIEW_IMG_WIDTH = Inches(6)
PAGE_NAME = 'page{}.png'

class Viewer(ExtensionsBase):
    def init_app(self, app):
        print('viewer init app')
        self.local = os.getcwd() != '/app'
        self.create_tmp()
        self._register_app(app, ext_name='viewer')
    
    # Create temporary folder to store survey view files
    def create_tmp(self):
        try:
            os.mkdir(TMPDIR)
        except:
            pass
        os.chdir(TMPDIR)
        try:
            os.remove(SURVEY_VIEW_ZIP)
        except:
            pass
        os.chdir('..')
    
    # Download the survey view for a give participant
    def survey_view(self, part):
        print('viewer survey view')
        self.part = part
        print('participant', self.part)
        self.create_files()
        path = os.path.join(os.getcwd(), TMPDIR, SURVEY_VIEW_ZIP)
        print('path', path)
        return send_file(
            path, mimetype='zip', 
            attachment_filename=SURVEY_VIEW_ZIP, as_attachment=True)
        
    # Create survey view files
    def create_files(self):
        print('create files')
        self.setup_pages()
        print(self.page_html)
        print(self.css)
        print(self.config)
        os.chdir(TMPDIR)
        self.doc = Document()
        self.zipf = zipfile.ZipFile(SURVEY_VIEW_ZIP, 'w', zipfile.ZIP_DEFLATED)
        [self.process_page(i, p) for i, p in enumerate(self.page_html)]
        self.doc.save(SURVEY_VIEW_DOC)
        self.zipf.write(SURVEY_VIEW_DOC)
        os.remove(SURVEY_VIEW_DOC)
        self.zipf.close()
        os.chdir('..')
        
    # Set up for creating survey view files
    # render page html and get css and config for imgkit
    def setup_pages(self):
        print('setup')
        self.page_html = [render_template('survey_view.html', page=Markup(p))
            for p in self.part._page_html]
        cssdir = url_for('static', filename='css/')[1:]
        print('cssdir', cssdir)
        cssdir = os.path.join(os.getcwd(), cssdir).replace('\\','/')
        print(cssdir)
        self.css = [cssdir+cssfile 
            for cssfile in ['default.min.css', 'bootstrap.min.css']]
        if self.local:
            self.config = imgkit.config()
        else:
            print('wkhtmltoimage', os.environ.get('WKHTMLTOIMAGE'))
            self.config = imgkit.config(
                wkhtmltoimage=os.environ.get('WKHTMLTOIMAGE'))
        
    # Process page
    # create png file
    # add to document
    # add to zip file
    def process_page(self, page_num, page_html):
        page_name = PAGE_NAME.format(page_num)
        imgkit.from_string(
            page_html, page_name, css=self.css, config=self.config, 
            options={'quiet':''})
        self.doc.add_picture(page_name, width=SURVEY_VIEW_IMG_WIDTH)
        self.zipf.write(page_name)
        os.remove(page_name)