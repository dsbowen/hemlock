"""url_for

Similar to Flask's `url_for`, except that it will return 'URL_UNAVAILABLE' when an exception is raised. This is useful for debugging outside a request context, such as in the shell.
"""

from flask import url_for as try_url_for

def url_for(*args, **kwargs):
    try:
        return try_url_for(*args, **kwargs)
    except:
        return 'URL_UNAVAILABLE'