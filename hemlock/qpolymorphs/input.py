
from hemlock.qpolymorphs.utils import *

from random import randint
from string import ascii_letters, digits


class Input(InputGroup, InputBase):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'input'}

    @Question.init('Input')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('input.html', q=self)
        return {'page': page, **kwargs}

    @property
    def input_type(self):
        return self.input.get('type')

    @input_type.setter
    def input_type(self, val):
        self.input['type'] = val
        self.body.changed()


def debug_fn(question, driver):
    """Text input debug function
    
    Possible actions:
    1. Leave the question blank
    2. Enter a number
        2.1. Integer
        2.2. Float
    3. Enter random string of letters, digits, and whitespace
    """
    inpt = question.get_input(driver)
    if inpt.get_attribute('type') == 'text':
        return
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
    chars = list(chars) + [' '] * int(.1*len(chars))
    length = int(random() * 10**randint(1,3))
    return ''.join([choice(chars) for i in range(length)])

def debug_fn(question, driver):
    """Text input debug function
    
    Possible actions:
    1. Leave the question blank
    2. Enter a number
        2.1. Integer
        2.2. Float
    3. Enter random string of letters, digits, and whitespace
    """
    inpt = question.get_input(driver)
    if inpt.get_attribute('type') == 'text' or inpt.tag_name == 'textarea':
        return
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
    chars = list(chars) + [' '] * int(.1*len(chars))
    length = int(random() * 10**randint(1,3))
    return ''.join([choice(chars) for i in range(length)])
    
@Settings.register('Input')
def settings():
    return {
        'debug_functions': debug_fn,
    }