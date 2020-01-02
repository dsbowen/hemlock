"""Utilities"""

def _correct_choices(question):
    """Indicate whether participant selected the correct choices

    If the participant can only select one choice, indicate whether the 
    participant selected one of the correct choices.
    """
    correct = [c for c in question.choices if c.value]
    if question.multiple:
        return question.response == correct
    return question.response in correct