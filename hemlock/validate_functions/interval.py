"""Interval validation"""

def interval(q, inf=None, sup=None, interval_type='closed', error_msg=None):
    """Interval may be closed, open, left-open, right-open, left-closed, or right-closed"""
    error_msg = error_msg or gen_error_msg(q, inf, sup, interval_type)
    if inf is not None and not valid_inf(q, inf, interval_type):
        return error_msg
    if sup is not None and not valid_sup(q, sup, interval_type):
        return error_msg

def valid_inf(q, inf, interval_type):
    data = type(inf)(q.response)
    if data > inf:
        return True
    if data < inf:
        return False
    # data == inf
    return interval_type in ['closed', 'left-closed', 'right-open']

def valid_sup(q, sup, interval_type):
    data = type(sup)(q.response)
    if data < sup:
        return True
    if data > sup:
        return False
    # data == sup
    return interval_type in ['closed', 'left-open', 'right-closed']

def gen_error_msg(q, inf, sup, interval_type):
    return '<p>Answer out of range.</p>'