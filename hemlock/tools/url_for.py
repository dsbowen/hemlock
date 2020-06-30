"""# url_for"""

from flask import url_for as try_url_for

def url_for(*args, **kwargs):
    """
    Attempt to return `flask.url_for(*args, **kwargs)`. However, this method 
    does not exit the program when getting a url outside a request context; 
    e.g. when debugging in a shell or notebook.

    Parameters
    ----------
    \*args, \*\*kwargs :
        Arguments and keyword arguments will be passed to `flask.url_for`.

    Returns
    -------
    url : str
        Output of `flask.url_for` if possible; otherwise `'URL_UNAVAILABLE'`.
    """
    try:
        return try_url_for(*args, **kwargs)
    except:
        return 'URL_UNAVAILABLE'