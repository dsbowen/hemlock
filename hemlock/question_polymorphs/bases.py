"""Question polymorph bases"""

from bs4 import Tag


class InputGroup():
    @property
    def prepend(self):
        return self.text('.prepend.input-group-text')

    @prepend.setter
    def prepend(self, val):
        self._set_input_group_div('prepend', val)

    @property
    def append(self):
        return self.text('.append.input-group-text')
    
    @append.setter
    def append(self, val):
        self._set_input_group_div('append', val)

    def _set_input_group_div(self, type_, val):
        input_group_div = self.select('.input-group-'+type_)
        if input_group_div is not None and val is None:
            return input_group_div.extract()
        if input_group_div is None:
            input_group_div = self._gen_input_group_div(type_)
        span = input_group_div.span
        if span is None:
            span = self._gen_input_group_text(type_)
        span.string = val
        self.soup = self.soup

    def _gen_input_group_div(self, type_):
        input_group_div = Tag(name='div')
        input_group_div['class'] = 'input-group-'+type_
        index = 0 if type_ == 'prepend' else -1
        self.select('.input-group').insert(index, input_group_div)
        return input_group_div

    def _gen_input_group_text(self, type_):
        span = Tag(name='span')
        span['class'] = type_ + ' input-group-text'
        input_group_div = self.select('.input-group-'+type_)
        if type_ == 'prepend':
            input_group_div.insert(0, span)
        else:
            input_group_div.append(span)
        return span