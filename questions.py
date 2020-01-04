"""Question polymorphs"""

import data_storage

from hemlock import *

@Settings.register('Page')
def settings():
    img = Img(
        src='/static/oid.png',
        alignment='center'
    )
    figure = img.body.select_one('figure')
    figure['style'] = 'padding-right:20%; padding-left:20%;'
    return {'back': True, 'icon': img.render()}

@Navigate.register
def QuestionPolymorphs(origin=None):
    b = Branch()
    Navigate.DataStorage(b)
    
    """Input"""
    p = Page(b)
    Input(p, label='<p>Inputs default to text inputs.</p>')
    Input(
        p, 
        label='<p>...but can be changed to any HTML input type. For example, a `color` input.</p>',
        input_type='color'
    )
    Input(
        p,
        label='<p>Inputs can have prepended and appended text and defaults.</p>',
        prepend='$',
        default=100,
        append='.00',
    )

    """Textarea"""
    p = Page(b)
    Textarea(p, label='<p>This is a textarea.</p>', rows=5)

    """Choice questions"""
    p = Page(b)
    Select(
        p,
        label='<p>This is a `Select` question.</p>',
        choices=['Red','Green','Blue']
    )
    Select(
        p,
        multiple=True,
        label='<p>Select questions can allow users to select multiple choices.</p>',
        choices=['World','Moon','Sun']
    )
    Check(
        p,
        label='<p>This is a `Check` question.</p>',
        choices=[1, 2, 3]
    )
    Check(
        p,
        multiple=True,
        label='<p>Check questions also can allow users to select multiple choices.</p>',
        choices=['foo','bar','baz']
    )
    Check(
        p,
        label='<p>This `Check` question displays in-line choices.</p>',
        inline=True,
        center=True,
        choices=list(range(1,6))
    )
    s = Select(
        p, 
        label='<p>You can set defaults for choice questions with the `default` attribute.</p>',
        choices=['Hello','Hola','Bonjour']
    )
    s.default = s.choices[2]
    c = Check(
        p,
        multiple=True,
        label='<p>You can set multiple defaults as well.</p>',
        choices=['Goodbye','Adios','Au revoir']
    )
    c.default = c.choices[1:3]

    """Range"""
    p = Page(b)
    Range(p, label='<p>This is a range input.</p>')
    Range(
        p,
        label='<p>This range input ranges from -10 to 10 in steps of 2.</p>',
        min=-10,
        max=10,
        step=2,
        default=-10
    )

    """File download"""
    p = Page(b)
    url = 'https://test-bucket2357.s3.us-east-2.amazonaws.com/hello_world.txt'
    Download(
        p,
        label='<p>This is a download button.</p>',
        downloads=[(url, 'hello-world.txt')]
    )

    """File upload"""
    # Use the `hlk gcloud-bucket` command to set up Google storage for file uploads
    p = Page(b)
    Label(p, label='Uploads are stored in your Google bucket.')
    File(
        p, 
        label='Upload a .jpg file.',
        filename='test-picture',
        allowed_extensions=['.jpg'],
    )

    return b