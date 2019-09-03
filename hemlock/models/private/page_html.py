##############################################################################
# Page Html model
# by Dillon Bowen
# last modified 09/02/2019
##############################################################################

import requests
import os
from hemlock.factory import db
from bs4 import BeautifulSoup
from base64 import b64encode
from PIL import Image, ImageOps
from io import BytesIO
from flask_login import current_user

# Video aspect ratio
ASPECT_RATIO = 16/9.0

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
        self.raw_html = html
        self.html = html
        self.part = current_user
        self.preprocess_html()
        
    # Preprocessing
    def preprocess_html(self):
        self._process(preprocess=True)
        
    # Main processing
    # return compiled html
    def process(self):
        self._process()
        return self.html
    
    # Store all images and videos as base64
    # convert only media to be copied for survey viewing during preprocessing
    def _process(self, preprocess=False):
        soup = BeautifulSoup(self.html, 'html.parser')
        images = soup.find_all('img')
        videos = soup.find_all('iframe')
        if preprocess:
            images = [i for i in images if i.has_attr('copy_for_viewing')]
            videos = [v for v in videos if v.has_attr('copy_for_viewing')]
        [self.encode_image(i) for i in images]
        [self.encode_video(soup, v) for v in videos]
        self.html = str(soup)
    
    # Encode an image in base64
    # if local, encode using absolute path
    # if url, encode using content from request
    # change image source to base64 data
    def encode_image(self, image):
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
    
    # Encode a video as a base64 image
    def encode_video(self, soup, video):
        try:
            buffer = BytesIO()
            thumbnail = self.create_thumbnail(video)
            thumbnail.save(buffer, format='png')
            data = b64encode(buffer.getvalue()).decode('utf-8')
        except:
            data = ''
        image = soup.new_tag('img')
        image.attrs = video.attrs
        image['src'] = 'data:image/png;base64,{}'.format(data)
        video.replace_with(image)
        
    # Create thumbnail
    # get raw thumbnail
    # get play button
    # paste play button onto thumbnail
    def create_thumbnail(self, video):
        thumbnail = self.get_raw_thumbnail(video)
        
        path = os.path.join(os.getcwd(), 'static/YouTube.png')
        play = Image.open(path.replace('\\', '/'))
        play = play.resize(thumbnail.size)
        
        thumbnail.paste(play, (0,0), play)
        return thumbnail
    
    # Get raw video thumbnail from url and pad to aspect ratio
    def get_raw_thumbnail(self, video):
        url = 'https://i4.ytimg.com/vi/{}/0.jpg'.format(video['vid'])
        thumbnail = Image.open(BytesIO(requests.get(url).content))
        width, height = thumbnail.size
        pad_vertical = width/float(height) > ASPECT_RATIO
        if pad_vertical:
            new_width, new_height = width, width // ASPECT_RATIO
        else:
            new_width, new_height = round(height * ASPECT_RATIO), height
        delta_w, delta_h = new_width-width, new_height-height
        padding = (
            delta_w//2, delta_h//2, 
            delta_w-(delta_w//2), delta_h-(delta_h//2))
        thumbnail = ImageOps.expand(thumbnail, padding)
        return thumbnail