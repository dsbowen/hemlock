

def require(q, message=None):
    data = q.get_data()
    if data is None or data == '':
        if message is not None:
            return message
        return "Please answer this question"
        
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