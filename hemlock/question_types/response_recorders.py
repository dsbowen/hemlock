"""Response recorders for Hemlock native question types"""

from hemlock.models import Question

@Question.register_response_recorder('embedded')
def record_embedded(question, response):
    return

@Question.register_response_recorder('text')
def record_text(question, response):
    return

@Question.register_response_recorder('free')
def record_free(question, response):
    question.data = question.response = question.default = response

@Question.register_response_recorder('single choice')
def record_single_choice(question, choice_id):
    """Record response for a single choice question type
    
    If participant did not select a choice, set default to None and return.
    Otherwise:
    1. Get the choice id (the input choice id is 'c<id>')
    2. Set question data and response to the value of the selected choice
    3. Set the default choice to the selected choice
    """
    if choice_id is None:
        question.default.choice = None
        return
    choice_id = choice_id[1:]
    for choice in question.choices:
        if choice.id == choice_id:
            response = choice.value
            break
    question.data = question.response = response
    question.default.choice = choice