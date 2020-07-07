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

    Inherits from [`hemlock.qpolymorphs.InputGroup`](input_group.md), 
    [`hemlock.models.InputBase`](bases.md), and 
    [`hemlock.Question`](question.md).

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
    Set up a 
    [Google bucket](https://cloud.google.com/storage/docs/creating-buckets)
    with the appropriate 
    [CORS permissions](https://cloud.google.com/storage/docs/cross-origin).

    Set an environment variable `BUCKET` to the name of the bucket, and 
    `GOOGLE_APPLICATION_CREDENTIALS` to the name of your 
    [Google application credentials JSON file](https://cloud.google.com/docs/authentication/getting-started).

    ```
    export BUCKET=<my-bucket> GOOGLE_APPLICATION_CREDENTIALS=<my-credentials.json>
    ```

    In `survey.py`:

    ```python
    from hemlock import Branch, File, Page, Label, route

    @route('/survey')
    def start():
    \    return Branch(
    \        Page(File(
    \            '<p>Upload a .png</p>', 
    \            filename='upload',
    \            allowed_extensions=['.png']
    \        )),
    \        Page(Label('<p>The End</p>'), terminal=True)
    \    )
    ```
    
    In `app.py`:

    ```python
    import survey

    from hemlock import create_app

    app = create_app()

    if __name__ == '__main__':
    \    from hemlock.app import socketio
    \    socketio.run(app, debug=True)
    ```

    Run the app locally with:

    ```
    $ python app.py # or python3 app.py
    ```

    And open your browser to <http://localhost:5000/>. Upload a .png and click to the next page. You'll find your uploaded file in your Google bucket in `participant-1/upload.png`.
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
        file_ = request.files.get(self.model_id)
        if file_ is None:
            # no file uploaded
            self.response = None
            return
        self.response = secure_filename(file_.filename)

    def _validate(self):
        """Verify that the uploaded file's mimetype is allowed"""
        if self.response and self.allowed_extensions:
            file_ = request.files.get(self.model_id)
            if file_.mimetype not in self.get_allowed_types():
                self.error = INVALID_MIMETYPE_MSG.format(
                    join('or', *self.allowed_extensions)
                )
                return False
        return super()._validate()