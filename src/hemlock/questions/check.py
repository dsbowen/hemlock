"""Check.
"""
from __future__ import annotations

import copy
from typing import Any

from ..app import db
from .choice_base import ChoiceQuestion


class Check(ChoiceQuestion):
    """Check.

    A check question allows users to select one or more choices by checking a box.

    Subclasses :class:`hemlock.questions.choice_base.ChoiceQuestion`.

    Args:
        *args (Any): Passed to :class:`hemlock.questions.choice_base.ChoiceQuestion` constructor.
        inline (bool, optional): Indicates that the choices will appear inline. Defaults
            to None.
        switch (bool, optional): Indicates that the check or radio button will be a
            switch. Defaults to None.
        **kwargs (Any): Passed to :class:`hemlock.questions.choice_base.ChoiceQuestion` constructor.
    """

    id = db.Column(db.Integer, db.ForeignKey("question.id"), primary_key=True)
    __mapper_args__ = {"polymorphic_identity": "check"}

    defaults = copy.deepcopy(ChoiceQuestion.defaults)
    defaults["template"] = "hemlock/check.html"
    defaults["html_settings"]["div"] = {"class": ["form-check"]}

    def __init__(
        self, *args: Any, inline: bool = None, switch: bool = None, **kwargs: Any
    ):
        super().__init__(*args, **kwargs)
        if inline is not None:
            self.set_inline(inline)
        if switch is not None:
            self.set_switch(switch)

    def set_inline(self, inline: bool = True) -> None:
        """Sets the choices to appear inline.

        Args:
            inline (bool, optional): Indicates that the choices will appear inline. If
                False, the choices will be stacked. Defaults to True.
        """
        self._add_or_remove_class("div", "form-check-inline", inline)

    def set_switch(self, switch: bool = True) -> None:
        """Indicates that the check or radio button will be a switch.

        Args:
            switch (bool, optional): Indicates that the check or radio button will be a
                switch. If False, the buttons will be ordinary check or radio buttons.
                Defaults to True.
        """
        self._add_or_remove_class("div", "form-switch", switch)
