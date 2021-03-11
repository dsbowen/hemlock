"""# Range sliders"""

from ..app import db, settings
from ..functions.debug import click_slider_range, drag_range, send_keys
from ..models import Question
from .bases import InputBase

import numpy as np
from flask import render_template

import json

choices_5 = [
    'Strongly disagree',
    'Disagree',
    'Neutral',
    'Agree',
    'Strongly agree'
]

choices_7 = [
    'Strongly disagree',
    'Disagree',
    'Slightly disagree',
    'Neutral',
    'Slightly agree',
    'Agree',
    'Strongly agree'
]

choices_9 = [
    'Very strongly disagree',
    'Strongly disagree',
    'Disagree',
    'Slightly disagree',
    'Neutral',
    'Slightly agree',
    'Agree',
    'Strongly agree',
    'Very strongly agree'
]

def likert(label=None, choices=5, default=0, **kwargs):
    """
    Create a Likert slider.

    Parameters
    ----------
    label : str, default=None

    choices : int or list, default=5
        A list of choices (str). May also be `5`, `7`, or `9` for default choice lists of length 5, 7, and 9. The list of choices should be an odd length and symmetric around the midpoint.

    default : int, default=0
        Default value. `0` is the scale midpoint.

    \*\*kwargs :
        Keyword arguments are passed to the `Slider` constructor.

    Returns
    -------
    Likert : `Slider`
    """
    def get_choices(choices):
        assert isinstance(choices, list) or choices in (5, 7, 9)
        if choices == 5:
            choices = choices_5
        elif choices == 7:
            choices = choices_7
        elif choices == 9:
            choices = choices_9
        return choices

    choices = get_choices(choices)
    tick_labels = [choices[i] for i in (0, int((len(choices)-1)/2), -1)]
    tick_labels = [label.replace(' ', '<br/>') for label in tick_labels]
    max_ = int((len(choices)-1)/2)
    min_ = -max_
    return Slider(
        label,
        ticks=[min_, 0, max_],
        ticks_labels=tick_labels,
        ticks_positions=[0, 50, 100],
        formatter=choices,
        default=default,
        **kwargs
    )

settings['Range'] = {
    'debug': drag_range,
    'type': 'range', 
    'class': ['custom-range'], 
    'min': 0, 'max': 100, 'step': 1
}


class Range(InputBase, Question):
    """
    Range sliders can be dragged between minimum and maximum values in step 
    increments.

    Inherits from [`hemlock.InputBase`](bases.md) and 
    [`hemlock.Question`](../models/question.md).

    Parameters
    ----------
    label : str or None, default=None
        Range label.

    template : str, default='hemlock/range.html'
        Template for the range body.

    Notes
    -----
    Ranges have a default javascript which displays the value of the range 
    slider to participants. This will be appended to any `js` and `extra_js`
    arguments passed to the constructor.

    Examples
    --------
    ```python
    from hemlock import Range, Page, push_app_context

    app = push_app_context()

    Page(Range('This is a range slider.')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'range'}

    def __init__(self, label=None, template='hemlock/range.html', **kwargs):
        super().__init__(label=label, template=template, **kwargs)
        self.js.append(render_template('hemlock/range.js', q=self))


settings['RangeInput'] = {
    'debug': send_keys,
    'width': '5em',
    'class': ['form-control'],
    'type': 'number', 'min': 0, 'max': 100, 'step': 1
}


class RangeInput(InputBase, Question):
    """
    Range slider with an input field.

    Inherits from [`hemlock.InputBase`](bases.md) and 
    [`hemlock.Question`](../models/question.md).

    Parameters
    ----------
    label : str or None, default=None
        Range label.

    template : str, default='hemlock/rangeinput.html'
        Template for the range body.

    width : str, default='5em'
        Width of the input field.

    Notes
    -----
    Ranges have a default javascript which displays the value of the range 
    slider to participants. This will be appended to any `js` and `extra_js`
    arguments passed to the constructor.

    Examples
    --------
    ```python
    from hemlock import RangeInput, Page, push_app_context

    app = push_app_context()

    Page(RangeInput('This is a range slider.')).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'rangeinput'}

    width = db.Column(db.String)

    def __init__(
            self, label=None, template='hemlock/rangeinput.html', **kwargs
        ):
        super().__init__(label=label, template=template, **kwargs)
        self.js.append(render_template('hemlock/rangeinput.js', q=self))


settings['Slider'] = {'debug': click_slider_range}

class Slider(InputBase, Question):
    """
    Bootstrap slider. 
    <a href="https://github.com/seiyria/bootstrap-slider" target="_blank">See here</a>.

    Inherits from [`hemlock.InputBase`](bases.md) and 
    [`hemlock.Question`](../models/question.md).

    Parameters
    ----------
    label : str or None, default=None
        Range label.

    template : str, default='hemlock/slider.html'

    Notes
    -----
    You can input the `formatter` parameter in one of three ways:

    1. Javascript function (str). <a href="https://seiyria.com/bootstrap-slider/#example-1" target="_blank">See here</a>.
    2. List of formatted values, one for each tick.
    3. Dictionary mapping tick values to formatted values. Any ticks not mapped to a formatted value are displayed as the tick value.

    Examples
    --------
    ```python
    from hemlock import Page, Slider, push_app_context

    app = push_app_context()

    Page(
    \    Slider(
    \        'This is a fancy Bootstrap slider',
    \        ticks=[0, 2, 4],
    \        ticks_labels=['very low', 'medium', 'high'],
    \        ticks_positions=[0, 50, 100],
    \        formatter=[
    \            'very low',
    \            'low',
    \            'medium',
    \            'high',
    \            'very high'
    \        ]
    \    )
    ).preview()
    ```
    """
    id = db.Column(db.Integer, db.ForeignKey('question.id'), primary_key=True)
    __mapper_args__ = {'polymorphic_identity': 'slider'}

    _input_attr_names = [
        'min', 'max', 'step',
        'precision',
        'orientation',
        'range',
        'selection',
        'tooltip',
        'tooltip_split',
        'tooltip_position',
        'handle',
        'reversed',
        'rtl',
        'enabled',
        'formatter',
        'natural_arrow_keys',
        'ticks',
        'ticks_positions',
        'ticks_labels',
        'ticks_snap_bounds',
        'ticks_tooltip',
        'scale',
        'focus',
        'labelledby',
        'rangeHighlights',
        'lock_to_tips'
    ]

    def __init__(self, label=None, template='hemlock/slider.html', **kwargs):
        self.input_attrs = {}
        super().__init__(label=label, template=template, **kwargs)

    def get_max(self):
        """
        Returns
        -------
        max : scalar
            Maximum value the slider can take.
        """
        if self.ticks:
            return self.ticks[-1]
        return 10 if self.max is None else self.max

    def get_min(self):
        """
        Returns
        -------
        min : scalar
            Minimum value the sldier can take.
        """
        if self.ticks:
            return self.ticks[0]
        return 0 if self.min is None else self.min

    def get_values(self):
        """
        Returns
        -------
        values : generator
            Range of values the slider can take.
        """
        step = 1 if self.step is None else self.step
        return np.arange(self.get_min(), self.get_max()+step, step).tolist()

    def get_midpoint(self):
        """
        Returns
        -------
        midpoint : scalar
            Scale midpoint.
        """
        values = self.get_values()
        return values[int(len(values)/2)]

    def _render_js(self):
        # gender bootstrap-slider javascript
        def set_value():
            # values is 1. response, 2. default, 3. scale midpoint
            if self.has_responded:
                value = self.response
            elif self.default is not None:
                value = self.default
            else:
                value = self.get_midpoint()
            slider_attrs['value'] = value

        def compile_formatter():
            formatter = slider_attrs.pop('formatter', None)
            if formatter is None:
                return
            if isinstance(formatter, list):
                # list of formatted values for each tick
                mapping = {
                    str(key): str(val) 
                    for key, val in zip(self.get_values(), formatter)
                }
                formatter = '''
                    function(value) {{
                        return {}[value];
                    }}
                '''.format(mapping)
            elif isinstance(formatter, dict):
                # mapping of tick values to formatted values
                mapping = {
                    str(key): str(val) for key, val in formatter.items()
                }
                formatter = '''
                    function(value) {{
                        var mapping = {};
                        if (mapping[value]){{
                            return mapping[value];
                        }}
                        return value;
                    }}
                '''.format(mapping)
            return formatter

        slider_attrs = self.input_attrs.copy()
        set_value()
        formatter = compile_formatter()
        slider_attrs = json.dumps(slider_attrs)
        if formatter:
            # slider_attrs is now a string ending in '}'
            # need to remove this, then insert formatter, then close with '}'
            slider_attrs = slider_attrs[:-1]+', formatter: '+formatter+'}'
        return render_template(
            'hemlock/slider.js', q=self, slider_attrs=slider_attrs
        )

    def _record_data(self):
        self.data = float(self.response)
        if (
            isinstance(self.get_min(), int)
            and isinstance(self.get_max(), int)
            and (self.step is None or isinstance(self.step, int))
        ):
            self.data = int(self.data)
        return self