"""Text input question"""

# init for other questions, page, etc
# make another input group question and see how much you can move
# input group question base

from hemlock.question_polymorphs.utils import *

from random import randint
from string import ascii_letters, digits


class Text(HTMLQuestion):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'text'}

    @HTMLQuestion.init('Text')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.soup = render_template('text_q.html', q=self)
        return {'page': page, **kwargs}

    def get_input(self, driver=None):
        """Get input from driver for debugging"""
        return driver.find_element_by_css_selector('#'+self.model_id)

    @property
    def textarea(self):
        inpt = self.select('#'+self.model_id)
        return inpt.name == 'textarea'

    @textarea.setter
    def textarea(self, val):
        assert isinstance(val, bool)
        name = 'textarea' if val else 'input'
        self.select('#'+self.model_id).name = name
        self.soup.changed()
    
    """Private methods"""
    def _render(self):
        value = self.response or self.default
        inpt = self.select('#'+self.model_id)
        if inpt is not None:
            inpt['value'] = value
        return self.soup.render()
    
    def _record_response(self, response):
        self.response = None if response == [''] else response[0]


def debug_func(question, driver):
    """Text input debug function
    
    Possible actions:
    1. Leave the question blank
    2. Enter a number
        2.1. Integer
        2.2. Float
    3. Enter random string of letters, digits, and whitespace
    """
    inpt = question.get_input(driver)
    if random() < .1:
        return
    if random() < .5:
        val = gen_number()
    else:
        val = gen_str()
    inpt.clear()
    inpt.send_keys(str(val))

def gen_number():
    num = random() * 10**randint(0,10)
    if random() < .1:
        num = -num
    if random() < .5:
        return int(num)
    return round(num, randint(0,10))

def gen_str():
    chars = ascii_letters + digits
    chars = list(chars) + [' '] * .1*int(len(chars))
    length = int(random() * 10**randint(1,3))
    return ''.join([choice(chars) for i in range(length)])

@Settings.register('Text')
def free_settings():
    return {
        'debug_functions': debug_func,
    }