"""InputGroup

`InputGroup` defines methods for interacting with a Bootstrap input-group.

An input-group has prepended and appended text wrapping the input.
"""

from hemlock.app import Settings, db
from hemlock.database import Question, ChoiceQuestion
from hemlock.database.bases import InputBase

from bs4 import Tag
from flask import render_template


class InputGroup():
    @property
    def prepend(self):
        return self.body.text('.input-group-prepend')

    @prepend.setter
    def prepend(self, val):
        self.body.set_element(
            '.input-group-prepend', val,
            target_selector='span.input-group-text', 
            gen_target=self._gen_input_group_text,
            args=['prepend']
        )

    @property
    def append(self):
        return self.body.text('.input-group-append')
    
    @append.setter
    def append(self, val):
        self.body.set_element(
            '.input-group-append', val,
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
    
    def _render(self, body=None):
        """Remove prepend and append div Tags if they are empty"""
        body = body or self.body.copy()
        if not self.prepend:
            body.select_one('div.input-group-prepend').extract()
        if not self.append:
            body.select_one('div.input-group-append').extract()
        return super()._render(body)