"""Free response question"""

from hemlock.question_polymorphs.imports import *

from random import randint
from string import ascii_letters, digits


class Free(Question):
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'free'}

    prepend = db.Column(db.Text)
    placeholder = db.Column(db.Text)
    append = db.Column(db.Text)

    @property
    def _prepend(self):
        if self.prepend is None:
            return ''
        return PREPEND.format(q=self)

    @property
    def _placeholder(self):
        return self.placeholder or ''

    @property
    def _default(self):
        return self.response or self.default or ''

    @property
    def _append(self):
        if self.append is None:
            return ''
        return APPEND.format(q=self)

    def __init__(self, page=None, **kwargs):
        Debug(self, text_input_debug)
        super().__init__(['free_settings'], page, **kwargs)

    def get_input(self, driver):
        return driver.find_element_by_css_selector('input#'+self.model_id)
    
    def _render(self):
        return super()._render(content=INPUT_GROUP.format(q=self))
    
    def _record_response(self, response):
        self.response = None if response == [''] else response[0]


def text_input_debug(question, driver):
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
    inpt.send_keys(str(val))

def gen_number():
    num = random() * randint(1,10)
    if random() < .5:
        return int(num)
    return round(num, randint(0,10))

def gen_str():
    chars = ascii_letters + digits
    chars = list(chars) + [' '] * int(len(chars)*.1)
    length = 10**randint(0,10)
    return ''.join(choice(chars) for i in range(length))


INPUT_GROUP = """
<div class="input-group mb-3">
    {q._prepend}
    <input type="text" class="form-control" id="{q.model_id}" name="{q.model_id}" placeholder="{q._placeholder}" value="{q._default}">
    {q._append}
</div>
"""

PREPEND = """
<div class="input-group-prepend">
    <span class="input-group-text">{q.prepend}</span>
</div>
"""

APPEND = """
<div class="input-group-append">
    <span class="input-group-text">{q.append}</span>
</div>
"""