from flask import url_for as try_url_for

def url_for(*args, **kwargs):
    try:
        return try_url_for(*args, **kwargs)
    except:
        return 'URL_UNAVAILABLE'