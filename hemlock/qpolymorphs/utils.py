
from hemlock.app import Settings, db
from hemlock.database.question import Question, ChoiceQuestion

from bs4 import Tag
from flask import render_template


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
        if value is None:
            self.input.attrs.pop('value', None)
        else:
            self.input['value'] = value
        return super()._render()


class InputGroup():
    @property
    def prepend(self):
        return self.text('.input-group-prepend')

    @prepend.setter
    def prepend(self, val):
        self._set_element(
            val, 
            parent_selector='div.input-group-prepend',
            target_selector='span.input-group-text', 
            gen_target=self._gen_input_group_text,
            args=['prepend']
        )

    @property
    def append(self):
        return self.text('.input-group-append')
    
    @append.setter
    def append(self, val):
        self._set_element(
            val,
            parent_selector='div.input-group-append',
            target_selector='span.input-group-text',
            gen_target=self._gen_input_group_text,
            args=['append']
        )
    
    def _gen_input_group_text(self, type_):
        """Generate input group prepend/append <div> Tag
        
        `type_` is 'prepend' or 'append'
        """
        span = Tag(name='span')
        span['class'] = 'input-group-text'
        return span