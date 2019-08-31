##############################################################################
# Survey viewer class
# by Dillon Bowen
# last modified 08/30/2019
##############################################################################

import os
import imgkit
import zipfile
from hemlock.extensions.extensions_base import ExtensionsBase
from flask import current_app, url_for, render_template, Markup, send_file
from docx import Document
from docx.shared import Inches

SURVEY_VIEW_ZIP = 'survey_view.zip'
SURVEY_VIEW_DOC = 'survey_view.docx'
TMPDIR = 'tmp'
SURVEY_VIEW_IMG_WIDTH = Inches(6)
ZOOM = 1.5
PAGE_NAME = 'page{}.png'

class Viewer(ExtensionsBase):
    # Initialize with application
    # create temp folder for storing survey view zip file
    # register to application
    def init_app(self, app):
        self.create_tmp()
        self._register_app(app, ext_name='viewer')
    
    # Create temporary folder to store survey view files
    # remove survey view zip file if it exists
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
    
    # Download the survey view for a given participant
    # create zipfile and send
    def survey_view(self, part):
        self.page_htmls = part._page_htmls.all()
        self.create_zipfile()
        path = os.path.join(os.getcwd(), TMPDIR, SURVEY_VIEW_ZIP)
        return send_file(
            path, mimetype='zip', 
            attachment_filename=SURVEY_VIEW_ZIP, as_attachment=True)
        
    # Create survey view files
    # create docx and zip files
    # add pages to docx and zip files
    # save docx and write to zip file
    def create_zipfile(self):
        self.setup_pages()

        os.chdir(TMPDIR)
        self.doc = Document()
        self.zipf = zipfile.ZipFile(SURVEY_VIEW_ZIP, 'w', zipfile.ZIP_DEFLATED)
        [self.store_page(i, p) for i, p in enumerate(self.page_htmls)]
        self.doc.save(SURVEY_VIEW_DOC)
        self.zipf.write(SURVEY_VIEW_DOC)
        os.remove(SURVEY_VIEW_DOC)
        self.zipf.close()
        os.chdir('..')
        
    # Set up for creating survey view files
    # render page html and get css and config for imgkit
    def setup_pages(self):
        self.page_htmls = [self.format_page(p) for p in self.page_htmls]
        cssdir = url_for('static', filename='css/')[1:]
        cssdir = os.path.join(os.getcwd(), cssdir).replace('\\','/')
        self.css = [cssdir+cssfile 
            for cssfile in ['default.min.css', 'bootstrap.min.css']]
        wkhtmltoimage_location = current_app.config['WKHTMLTOIMAGE']
        self.config = imgkit.config(wkhtmltoimage=wkhtmltoimage_location)
    
    # Format html for compatibility with wkhtmltopdf
    def format_page(self, page_html):
        page_html = page_html.process()
        return render_template('survey_view.html', page=Markup(page_html))
        
    # Store page
    # create png file
    # add to document
    # add to zip file
    def store_page(self, page_num, page_html):
        page_name = PAGE_NAME.format(page_num)
        imgkit.from_string(
            page_html, page_name, css=self.css, config=self.config, 
            options={'quiet':'', 'quality':100, 'zoom':ZOOM})
        self.doc.add_picture(page_name, width=SURVEY_VIEW_IMG_WIDTH)
        self.zipf.write(page_name)
        os.remove(page_name)