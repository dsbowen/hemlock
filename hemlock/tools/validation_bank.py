###############################################################################
# Bank of validation functions
# by Dillon Bowen
# last modified 04/03/2019
###############################################################################

import re

# Require a response
def require(q, message=None):
    data = q.get_data()
    if data is None or data == '':
        if message is not None:
            return message
        return '<p>Please answer this question.</p>'
        
# Data should be an integer
def integer(q, message=None):
    data = q.get_data()
    if data is None or data == '':
        return
    try:
        int(data)
        return
    except:
        if message is not None:
            return message
        return '<p>Please enter a number without decimals.</p>'
        


###############################################################################
# isin validation function
# check that data is in a given set or interval
###############################################################################
        
# Data should be in a specified set or interval
# arguments:
    # set: iterable
    # interval: 4-tuple interval notation e.g. ('(', '-infty', 0, ']')
    # '-infty' and 'infty' represent (negative) infinity
    # message: error message, string
# return if question does not have data
# check that set xor interval is specified
# check if data is in the given set or interval
def isin(q, set=None, interval=None, message=None):
    data = q.get_data()
    if data is None or data == '':
        return

    _check_set_xor_interval(set, interval, func_name='isin')
    
    if set is not None and not _isin_set(data, set):
        return _isin_set_error_message(set, message)
    if interval is not None and not _isin_interval(data, interval):
        return _isin_interval_error_message(interval, message)
    
# Check that set and interval are not both specified
def _check_set_xor_interval(set, interval, func_name):
    if set is not None and interval is not None:
        raise ValueError(
            '{0} does not accept both a set and an interval'.format(name))
    
# Check if data is in a given set
# check that the set is iterable
# search for a match to the data in set
# return bool indicating that match was found
def _isin_set(data, set):
    _check_valid_set(set)

    for item in set:
        try:
            temp_data = type(item)(data)
            if temp_data == item:
                return True
        except:
            pass
            
    return False
    
# Check for a valid set (i.e. iterable)
# if not, raise error
def _check_valid_set(set):
    try:
        iter(set)
    except:
        raise TypeError('set should be iterable')
    
# Return error message if data is not in set
def _isin_set_error_message(set, message):
    if message is not None:
        return message
    return (
        '<p>Your answer should be one of the following: '
        +', '.join(str(i) for i in set)
        +'.</p>')
        
# Check if data is in a given interval
# check if interval is valid (i.e. 4-tuple in interval notation)
# parse interval
# return bool indicating that data is in interval
def _isin_interval(data, interval): 
    _check_valid_interval(interval)
    min, max, min_strict, max_strict = _parse_interval(interval)
  
    return (
        (min == '-infty' and max == 'infty')
        or (min == '-infty' and _max(data, max, max_strict))
        or (max == 'infty' and _min(data, min, min_strict))
        or (_min(data, min, min_strict) and (_max(data, max, max_strict))))
    
# Check that the interval is valid
# i.e. that it is a 4-tuple following interval notation
def _check_valid_interval(interval):
    if (len(interval) == 4 
        and interval[0] in ('(','[') and interval[3] in (')',']')):
        return
    raise ValueError('''
        Interval should be a 4-tuple following set notation 
        e.g. ('(', '-infty', 0, ']')''')
        
# Parse an interval (4-tuple in interval notation)
# into min, max, min_strict, max_strict
def _parse_interval(interval):
    return (interval[1], interval[2], interval[0]=='(', interval[3]==')')
    
# Check that data is less than (or equal to) max
def _max(data, max, strict):
    try:
        temp_data = type(max)(data)
    except:
        raise TypeError('data cannot be converted to type(max)')

    return temp_data < max or (not strict and temp_data == max)
    
# Check that data is greater than (or equal to) min
def _min(data, min, strict, message=None):
    try:
        temp_data = type(min)(data)
    except:
        raise TypeError('data cannot be converted to type(min)')
        
    return temp_data > min or (not strict and temp_data == min)

# Return error message for data not in interval error
# cases:
    # upper bound only
    # lower bound only
    # both upper and lower bound
        # open interval
        # left open, right closed (x,y]
        # left closed, right open [x,y)
        # closed interval
            # interval includes 1 element (i.e. min==max)
            # interval includes infite elements
def _isin_interval_error_message(interval, message):
    if message is not None:
        return message

    min, max, min_strict, max_strict = _parse_interval(interval)
    
    if min == '-infty':
        return _max_error_message(max, max_strict)
    if max == 'infty':
        return _min_error_message(min, min_strict)

    if min_strict and max_strict:
        return '''
        <p>Your answer should be between {0} and {1}.</p>
        '''.format(min, max)
    if min_strict and not max_strict:
        return '''
        <p>Your answer should be more than {0} and at most {1}.</p>
        '''.format(min, max)
    if not min_strict and max_strict:
        return '''
        <p>Your answer should be at least {0} and less than {1}.</p>
        '''.format(min, max)
    if min == max:
        return '''
        <p>Your answer should be exactly {0}.</p>
        '''.format(min)
    return '''
        <p>Your answer should be between {0} and {1} (inclusive).</p>
        '''.format(min, max)
        
# Return error message if data is greater than (or equal to) the maximum
def _max_error_message(max, strict):
    if strict:
        return '<p>Your answer should be less than {0}.</p>'.format(max)
    return '<p>Your answer should be at most {0}.</p>'.format(max)

# Return error message if data is less than (or equal to) the minimum
def _min_error_message(min, strict):
    if strict:
        return '<p>Your answer should be more than {0}.</p>'.format(min)
    return '<p>Your answer should be at least {0}.</p>'.format(min)


###############################################################################
# decimals validation function
# check that number of decimals is in a given set or interval
###############################################################################

# Number of decimals should be within a set or specified interval
# check that the data is in numeric format
# check that interval is a 4-tuple using interval notation
# compute number of decimals
# check if number of decimals is in set or interval
def decimals(q, set=None, interval=None, message=None):
    data = q.get_data()
    if data is None or data == '':
        return
        
    try:
        float(data)
    except:
        return 'Please enter a number'
        
    _check_set_xor_interval(set, interval, func_name='decimals')
    num_decimals = _get_num_decimals(data)
    
    if set is not None and not _isin_set(num_decimals, set):
        return _decimals_set_error_message(set, message)
    if interval is not None and not _isin_interval(num_decimals, interval):
        return _decimals_interval_error_message(interval, message)
        
# Return the number of decimals given a number (or string)
def _get_num_decimals(data):
    split = str(data).split('.')
    if len(split) == 1:
        return 0
    return len(split[1])

# Return error message if number of decimals not in set
def _decimals_set_error_message(set, message):
    if message is not None:
        return message
        
    if len(set) == 1:
        return 'Your answer should contain exactly {0} decimals'.format(set[0])
    set, last = set[:-1], set[-1]
    return (
        '<p>Your answer should contain '
        +', '.join([str(i) for i in set])
        +' or {0} decimals.</p>'.format(last))
        
# Return error message if number of decimals not in interval
# cases:
    # upper bound only
    # lower bound only
    # both upper and lower bound
        # open interval
        # left open, right closed (x,y]
        # left closed, right open [x,y)
        # closed interval
            # interval includes 1 element (i.e. min==max)
            # interval includes infite elements
def _decimals_interval_error_message(interval, message):
    if message is not None:
        return message

    min, max, min_strict, max_strict = _parse_interval(interval)
    
    if min == '-infty':
        return _max_decimals_error_message(max, max_strict)
    if max == 'infty':
        return _min_decimals_error_message(min, min_strict)

    if min_strict and max_strict:
        return '''
        <p>Your answer should contain between {0} and {1} decimals.</p>
        '''.format(min, max)
    if min_strict and not max_strict:
        return '''
        <p>Your answer should contain more than {0} and at most {1} decimals.</p>
        '''.format(min, max)
    if not min_strict and max_strict:
        return '''
        <p>Your answer should contain at least {0} and fewer than {1} decimals.</p>
        '''.format(min, max)
    if min == max:
        return '''
        <p>Your answer should contain exactly {0} decimals.</p>
        '''.format(min)
    return '''
        <p>Your answer should contain between {0} and {1} decimals (inclusive).</p>
        '''.format(min, max)
        
# Return error message if number of decimals exceeds the maximum
def _max_decimals_error_message(max, strict):
    if strict:
        return '<p>Your answer should contain fewer than {0} decimals.</p>'.format(max)
    return '<p>Your answer should contain at most {0} decimals.</p>'.format(max)

# Return error message if number of decimals deceeds the minimum
def _min_decimals_error_message(min, strict):
    if strict:
        return '<p>Your answer should contain more than {0} decimals.</p>'.format(min)
    return '<p>Your answer should contain at least {0} decimals.</p>'.format(min)