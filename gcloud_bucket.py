"""Google Cloud Bucket

If you have the hemlock-cli, use `hlk gcloud-bucket` to create Google Cloud 
buckets.
"""

import workers

from hemlock import *

# @route('/survey')
@Navigate.register
def GCloudBucket(origin=None):
    b = Branch()
    # Navigate.Workers(b)
    Navigate.End(b)

    p = Page(b)
    Label(
        p,
        label='<p>Buckets are useful for several purposes, including embedding images and uploading and downloading files.</p>'
    )

    """Embed images"""
    img = Img(
        caption='Computer Problems',
        alignment='center',
        src=src_from_bucket('computer_problems.png')
    )
    Label(p, label=img.render())

    """Download files"""
    url = url_from_bucket('computer_problems.png')
    Download(p, downloads=[(url, 'computer_problems')])

    """Uploaded files"""
    File(
        p, 
        label='Upload a .jpg file.',
        filename='test-picture',
        allowed_extensions=['.jpg'],
    )

    return b