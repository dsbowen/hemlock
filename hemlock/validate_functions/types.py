"""Validates that response is of the correct type"""

NUMERIC_ERROR_MSG = '<p>Please enter a number.</p>'

def numeric(q):
    try:
        float(q.response)
    except:
        return NUMERIC_ERROR_MSG