

def convert_data(question, new_type, *args, **kwargs):
    question.data = new_type(question.data, *args, **kwargs)

def convert_response(question, new_type, *args, **kwargs):
    question.response = new_type(question.response, *args, **kwargs)