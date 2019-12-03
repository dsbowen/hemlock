ERROR_MSG = '<p>Please answer this question.</p>'

def require(q):
    return ERROR_MSG if q.response is None else None