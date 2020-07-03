"""# File upload"""

from ..app import db, settings
from ..models import InputBase, Question
from ..tools import join
from .input_group import InputGroup

from flask import current_app, render_template, request
from sqlalchemy_mutable import MutableListType
from werkzeug.utils import secure_filename

import os
from datetime import timedelta
from mimetypes import types_map

INVALID_MIMETYPE_MSG = """
<p>Please upload a file with one of the following extensions: {}.
"""

def upload_to_bucket(file_):
    """
    Default `hemlock.File` submit function. Uploads a participant file to 
    Google bucket.

    Parameters
    ----------
    file_ : hemlock.File
    """
    path = file_.get_path()
    upload = request.files.get(file_.model_id)
    if not (path and upload):
        return
    blob = current_app.gcp_bucket.blob(path)
    if path.endswith('.txt'):
        # .txt files require mimetype 'text/html' 
        # rather than the default 'text/plain'
        blob.upload_from_string(upload.read(), content_type='text/html')
        return
    blob.upload_from_string(upload.read())  
        
settings['File'] = {'submit_functions': upload_to_bucket}


class File(InputGroup, InputBase, Question):
    """
    Allows participants to upload files.

    Inherits from [`hemlock.InputGroup`](input_group.md), 
    [`hemlock.InputBase`](bases.md), and [`hemlock.Question`](question.md).

    Parameters
    ----------
    label : str or bs4.BeautifulSoup, default=''
        Upload file label.

    template : str, default='hemlock/file.html'
        Template for the file upload body.

    Attributes
    ----------
    allowed_extensions : list
        Allowed file extensions, e.g. `['.png','.jpeg']`.

    filename : str
        Name of the file as stored in the Google bucket.

    Examples
    --------
    ```python
    from hemlock import File, Page, push_app_context

    push_app_context()

    p = Page([File('<p>Upload a .png file.</p>', allowed_extensions=['.png'])])
    p.preview('Ubuntu')
    p.preview() # p.preview('Ubuntu') if working in Ubuntu/WSL
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'file'}

    allowed_extensions = db.Column(MutableListType)
    filename = db.Column(db.String)

    def __init__(self, label='', template='hemlock/file.html', **kwargs):
        super().__init__(label, template, **kwargs)
        self.js = render_template('hemlock/file.js', self_=self)

    def generate_signed_url(self, expiration=timedelta(hours=.5), **kwargs):
        """
        Generate a signed URL for the uploaded file.

        Parameters
        ----------
        expiration : datetime.timedelta, default=datetime.timedelta(0, 1800)
            Duration for which this signed URL is valid.

        \*\*kwargs :
            Additional keyword arguments are passed to the 
            `generate_signed_url` method.
        
        Notes
        -----
        Read more about [signed URLs](https://cloud.google.com/storage/docs/access-control/signed-urls).
        """
        path = self.get_path()
        if not (path and self.response):
            return
        blob = current_app.gcp_bucket.blob(path)
        return blob.generate_signed_url(expiration=expiration, **kwargs)

    def get_allowed_types(self):
        """
        Returns
        -------
        allowed_types : list
            List of allowed mimetypes. Derived from `self.allowed_extensions`.
        """
        if self.allowed_extensions:
            return set([types_map[ext] for ext in self.allowed_extensions])

    def get_path(self):
        """        
        Returns
        -------
        path : str
            Path to the uploaded file in the Google bucket.
        """
        if not self.filename:
            return
        if self.filename.startswith('/'):
            # absolute path
            path = self.filename
        else:
            # relative path in participant's folder
            # participant's folder is `part.model_id`
            path = os.path.join(self.part.model_id, self.filename)
        if self.response and '.' in self.response:
            # add the extension of the participant's response to the path
            # note: response is the name of the uploaded file
            path += '.' + self.response.split('.')[-1]
        return path

    def _record_response(self):
        """Record response as name of uploaded file"""
        if request.files.get(self.model_id) is None:
            # no file uploaded
            self.response = None
            return
        self.response = secure_filename(self.upload.filename)

    def _validate(self):
        """Verify that the uploaded file's mimetype is allowed"""
        if self.upload and self.allowed_extensions:
            if self.upload.mimetype not in self.get_allowed_types():
                self.error = INVALID_MIMETYPE_MSG.format(
                    join('or', *self.allowed_extensions)
                )
                return False
        return super()._validate()