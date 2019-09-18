"""Html database type

Converts to string on bind. Returns Markup on process result.
"""

from flask import Markup
from sqlalchemy.types import Text, TypeDecorator


class HtmlType(TypeDecorator):
    impl = Text

    def process_bind_param(self, value, dialect):
        return str(value)
    
    def process_result_value(self, value, dialect):
        return Markup(value)