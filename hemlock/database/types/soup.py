
from bs4 import BeautifulSoup
from flask import Markup
from sqlalchemy import PickleType
from sqlalchemy.ext.mutable import Mutable

from copy import copy


class MutableSoup(Mutable, BeautifulSoup):
    @classmethod
    def coerce(cls, key, obj):
        if isinstance(obj, cls):
            return obj
        if isinstance(obj, str):
            return cls(obj, 'html.parser')
        if isinstance(obj, BeautifulSoup):
            return cls(str(obj), 'html.parser')
        return super().coerce(key, obj)

    def copy(self):
        return copy(self)

    def _render(self):
        return Markup(str(self))

    def __getstate__(self):
        d = self.__dict__.copy()
        d.pop('_parents', None)
        return d


class MutableSoupType(PickleType):
    pass


MutableSoup.associate_with(MutableSoupType)