###############################################################################
# Bank of validation functions
# by Dillon Bowen
# last modified 03/12/2019
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
    
# Data must be within a given range
def in_range(q, *, min, max, message=None):
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
        
'''
def in_range(q, args):
    min, max= args[0:2]
    data = q.get_data()
    if data is None or data == '':
        return
    try:
        data = type(min)(data)
    except:
        return 'Please enter the correct type of data'
    try:
        message = args[2]
    except:
        message = 'Your answer should be between {0} and {1}'.format(min, max)
    if not min <= data <= max:
        return message
'''