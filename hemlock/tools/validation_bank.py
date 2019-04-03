###############################################################################
# Bank of validation functions
# by Dillon Bowen
# last modified 04/03/2019
###############################################################################

# Require a response
def require(q, message=None):
    data = q.get_data()
    if data is None or data == '':
        if message is not None:
            return message
        return "Please answer this question"
        
# Data must be an integer
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
        return 'Please enter a number without decimals'
        


###############################################################################
# isin validation function
# check that data is in a given set or interval
###############################################################################
        
# Data must be in a specified set or interval
# arguments:
    # set: iterable
    # interval: 4-tuple interval notation e.g. ('(', '-infty', 0, ']')
    # '-infty' and 'infty' represent (negative) infinity
    # message: error message, string
# return if question does not have data
# check that set or interval is specified but not both
# check if data is in the given set or interval
def isin(q, set=None, interval=None, message=None):
    data = q.get_data()
    if data is None or data == '':
        return

    if set is None and interval is None:
        raise ValueError(
            'isin requires either a set or an interval')
    if set is not None and interval is not None:
        raise ValueError(
            'isin does not accept both a set and an interval')
    
    if set is not None:
        return _isin_set(data, set, message)
    return _isin_interval(data, interval, message)
    
# Check if data is in a given set
# check that the set is iterable
# search for a match to the data in set
# return error message if no match is found
def _isin_set(data, set, message):
    _check_valid_set(set)

    for item in set:
        try:
            temp_data = type(item)(data)
            if temp_data == item:
                return
        except:
            pass
            
    if message is not None:
        return message
    return ('Your answer should be one of the following: '
        +', '.join(str(i) for i in set))
        
# Check for a valid set (i.e. iterable)
# if not, raise error
def _check_valid_set(set):
    try:
        iter(set)
    except:
        raise TypeError('set must be iterable')
        
# Check if data is in a given interval
# check that the interval is valid and parse
# check if data is in interval
# if not, return error message
def _isin_interval(data, interval, message):
    _check_valid_interval(interval)
    min, max, min_strict, max_strict = _parse_interval(interval)
    
    if min == '-infty' and max == 'infty':
        return
    if min == '-infty':
        return _max(data, max, max_strict, message)
    if max == 'infty':
        return _min(data, min, min_strict, message)
    if not any((_max(data, max, max_strict), _min(data, min, min_strict))):
        return
        
    if message is not None:
        return message
    return _interval_error_message(min, max, min_strict, max_strict)
    
# Check that the interval is valid
# i.e. that it is a 4-tuple following interval notation
def _check_valid_interval(interval):
    if (len(interval) == 4 
        and interval[0] in ('(','[') and interval[3] in (')',']')):
        return
    raise ValueError('''
        Interval is a 4-tuple following set notation 
        e.g. ('(', '-infty', 0, ']')''')
        
# Parse an interval (4-tuple in interval notation)
# into min, max, min_strict, max_strict
def _parse_interval(interval):
    return (interval[1], interval[2], interval[0]=='(', interval[3]==')')
    
# Check that data is less than max
def _max(data, max, strict, message=None):
    try:
        temp_data = type(max)(data)
    except:
        raise TypeError('data cannot be converted to type(max)')

    if temp_data < max or (not strict and data == max):
        return
        
    if message is not None:
        return message
    if strict:
        return 'Your answer should be less than {0}'.format(max)
    return 'Your answer should be at most {0}'.format(max)
    
# Check that data is greater than min
def _min(data, min, strict, message=None):
    try:
        temp_data = type(min)(data)
    except:
        raise TypeError('data cannot be converted to type(min)')
        
    if temp_data > min or (not strict and data == min):
        return
        
    if message is not None:
        return message
    if strict:
        return 'Your answer should be more than {0}'.format(min)
    return 'Your answer should be at least {0}'.format(min)

# Return error message for data not in interval error
def _interval_error_message(min, max, min_strict, max_strict):
    if min_strict and max_strict:
        return '''
        Your answer should be between {0} and {1}
        '''.format(min, max)
    if min_strict and not max_strict:
        return '''
        Your answer should be more than {0} and at most {1}
        '''.format(min, max)
    if not min_strict and max_strict:
        return '''
        Your answer should be at least {0} and less than {1}
        '''.format(min, max)
    return '''
        Your answer should be between {0} and {1} (inclusive)
        '''.format(min, max)
    
# Data must be within a given range
def in_range(q, min, max, message=None):
    data = q.get_data()
    if data is None or data == '':
        return
        
    try:
        data = type(min)(data)
    except:
        return 'Please enter the correct type of data'
        
    if min <= data <= max:
        return
        
    if message is not None:
        return message
    return 'Your answer should be between {0} and {1}'.format(min, max)