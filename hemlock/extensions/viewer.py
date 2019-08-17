##############################################################################
# Survey viewer class
# by Dillon Bowen
# last modified 08/17/2019
##############################################################################

import os
import imgkit
from hemlock.extensions.extensions_base import ExtensionsBase
from flask import url_for, render_template, Markup

SURVEY_VIEW_ZIP = 'survey_view.zip'
TMPDIR = 'tmp'

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
        return 'hello world'
        
    # Create survey view files
    def create_files(self):
        print('create files')
        self.setup_pages()
        print(self.page_html)
        print(self.css)
        print(self.config)
        
    # Set up for creating survey view files
    # render page html and get css and config for imgkit
    def setup_pages(self):
        print('setup')
        self.page_html = [render_template('survey_view.html', page=Markup(p))
            for p in self.part._page_html]
        cssdir = url_for('static', filename='css/')[1:]
        cssdir = os.path.join(os.getcwd(), cssdir).replace('\\','/')
        self.css = [cssdir+cssfile 
            for cssfile in ['default.min.css', 'bootstrap.min.css']]
        if self.local:
            self.config = imgkit.config()
        else:
            self.config = imgkit.config(
                wkhtmltoimage=os.environ.get('WKHTMLTOIMAGE'))