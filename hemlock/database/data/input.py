"""Generic Input model"""

from hemlock.database.data.utils import *

from random import randint
from string import ascii_letters, digits


class InputBase(Question):
    @property
    def input(self):
        return self.body.select_one('#'+self.model_id)

    def get_input_from_driver(self, driver=None):
        """Get input from driver for debugging"""
        return driver.find_element_by_css_selector('#'+self.model_id)

    def _render(self):
        """Set the default value before rendering"""
        value = self.response or self.default
        inpt = self.input
        if inpt.name == 'textarea':
            inpt.string = value or ''
        elif value is None:
            inpt.attrs.pop('value', None)
        else:
            inpt['value'] = value
        return self.body


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

    @property
    def textarea(self):
        return self.input.name == 'textarea'

    @textarea.setter
    def textarea(self, val):
        """Change question from text input to textarea (or vice versa)

        This method creates a new Tag with the appropriate input type. Note 
        that it is not enough to change the name of the Tag, as 
        BeautifulSoup parser automatically converts <input></input> to 
        <input/>. Changing the Tag name to 'textarea' produces <textarea/>, 
        whereas <textarea></textarea> is required.
        """
        assert isinstance(val, bool)
        if val == self.textarea:
            return
        name = 'textarea' if val else 'input'
        curr_input = self.input
        new_input = Tag(name=name)
        new_input.attrs = curr_input.attrs
        parent = curr_input.parent
        parent.insert(parent.index(curr_input), new_input)
        curr_input.extract()
        self.body.changed()


class Range(InputGroup, InputBase):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'range'}

    @Question.init('Range')
    def __init__(self, page=None, **kwargs):
        super().__init__()
        self.body = render_template('range.html', q=self)
        return {'page': page, **kwargs}
    
    