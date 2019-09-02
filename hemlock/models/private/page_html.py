##############################################################################
# Page Html model
# by Dillon Bowen
# last modified 08/30/2019
##############################################################################

import requests
import os
from hemlock.factory import db
from bs4 import BeautifulSoup
from base64 import b64encode
from flask_login import current_user

'''
Relationships:
    part: participant to whom the page html belongs

Columns:
    html: preprocessed or processed html
'''
class PageHtml(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    part_id = db.Column(db.Integer, db.ForeignKey('participant.id'))
    html = db.Column(db.String)
    
    # Store compiled html and add to participant
    # preprocess the html
    def __init__(self, html):   
        self.html = html
        self.part = current_user
        self.preprocess_html()
        
    # Preprocessing
    # store images as base64 if copy_for_viewing
    def preprocess_html(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        images = soup.find_all('img')
        [self.encode64(i) for i in images if i.has_attr('copy_for_viewing')]
        self.html = str(soup)
        
    # Main processing
    # store all images as base64
    # return compiled html
    def process(self):
        soup = BeautifulSoup(self.html, 'html.parser')
        images = soup.find_all('img')
        [self.encode64(i) for i in images]
        self.html = str(soup)
        return self.html
    
    # Encode an image in base64
    # if local, encode using absolute path
    # if url, encode using content from request
    # change image source to base64 data
    def encode64(self, image):
        src = image['src']
        if src.startswith('/'):
            path = os.path.join(os.getcwd(), src[1:]).replace('\\', '/')
            data = b64encode(open(path, 'rb').read()).decode('utf-8')
        elif src.startswith('http'):
            try:
                data = b64encode(requests.get(src).content).decode('utf-8')
            except:
                data = ''
        else:
            return
        image['src'] = 'data:image/png;base64,{}'.format(data)