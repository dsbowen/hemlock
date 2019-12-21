"""Question polymorph bases"""

from bs4 import Tag


class InputGroup():
    @property
    def prepend(self):
        return self.text('.prepend.input-group-text')

    @prepend.setter
    def prepend(self, val):
        self._set_element(
            val, 
            parent_selector='span.prepend-wrapper',
            target_selector='span.prepend.input-group-text', 
            gen_target=self._gen_input_group_div,
            args=['prepend']
        )

    @property
    def append(self):
        return self.text('.append.input-group-text')
    
    @append.setter
    def append(self, val):
        self._set_element(
            val,
            parent_selector='span.append-wrapper',
            target_selector='span.append.input-group-text',
            gen_target=self._gen_input_group_div,
            args=['append']
        )
    
    def _gen_input_group_div(self, type_):
        """Generate input group prepend/append <div> Tag
        
        `type` is 'prepend' or 'append'
        """
        input_group_div = Tag(name='div')
        input_group_div['class'] = 'input-group-'+type_
        span = Tag(name='span')
        span['class'] = [type_, 'input-group-text']
        input_group_div.append(span)
        return input_group_div