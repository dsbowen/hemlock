"""File upload"""

from hemlock.qpolymorphs.utils import *

from flask import current_app, request
from sqlalchemy_mutable import MutableListType
from werkzeug.utils import secure_filename

from datetime import timedelta
from mimetypes import types_map
import os


class File(InputGroup, InputBase, Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'file'}

    allowed_extensions = db.Column(MutableListType)
    filename = db.Column(db.String)

    @property
    def allowed_types(self):
        """Get allowed mimetypes from allowed extensions."""
        if self.allowed_extensions:
            return set([types_map[ext] for ext in self.allowed_extensions])

    @property
    def path(self):
        """Get Google bucket file path
        
        Filenames starting with '/' are treated as absolute paths. 
        Otherwise, this method assumes `filename` refers to a relative path 
        in a participant's folder.

        The extension of the participant's response (i.e. the name of the 
        uploaded file) is added to the path.
        """
        if not self.filename:
            return
        if self.filename.startswith('/'):
            path = self.filename
        else:
            path = os.path.join(self.part.model_id, self.filename)
        if self.response and '.' in self.response:
            path += '.' + '.'.join(self.response.split('.')[1:])
        return path

    @property
    def upload(self):
        """Get the uploaded file

        If no uploaded file is detected, get it from the form response.
        """
        if not hasattr(self, '_upload'):
            self._set_upload()
        return self._upload

    def _set_upload(self):
        self._upload = request.files.get(self.model_id)

    @Question.init('File')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('file.html', q=self)
        self.js = render_template('file.js', q=self)
        return {'page': page, **kwargs}

    def generate_signed_url(self, **kwargs):
        """Generate a signed URL for the uploaded file
        
        Note that the generate_signed_url` method requires an expiration.
        """
        path = self.path
        if not (path and self.response):
            return
        kwargs['expiration'] = kwargs.get('expiration') or timedelta(hours=.5)
        blob = current_app.gcp_bucket.blob(path)
        return blob.generate_signed_url(**kwargs)

    def _record_response(self):
        """Record response from file name"""
        self._set_upload()
        if self.upload is None:
            self.response = None
            return
        self.response = secure_filename(self.upload.filename)


INVALID_MIMETYPE_MSG = """
<p>Please upload a file with one of the following extensions: {}.
"""

def verify_mimetype(question):
    """Verify that the uploaded file is of the approparite mimetype"""
    if not (question.upload and question.allowed_extensions):
        return
    if question.upload.mimetype not in question.allowed_types:
        return INVALID_MIMETYPE_MSG.format(
            ', '.join(question.allowed_extensions)
        )

def upload_to_bucket(question):
    """Upload file to bucket
        
    Note that `response` is the name of the uploaded file. .txt files 
    require the mimetype 'text/html' rather than the default 'text/
    plain'.
    """
    path, upload = question.path, question.upload
    if not path or not upload:
        return
    blob = current_app.gcp_bucket.blob(path)
    if not path.endswith('.txt'):
        return blob.upload_from_string(upload.read())
    blob.upload_from_string(upload.read(), content_type='text/html')

@Settings.register('File')
def settings():
    return {
        'validate_functions': verify_mimetype,
        'submit_functions': upload_to_bucket,
    }