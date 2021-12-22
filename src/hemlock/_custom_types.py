from __future__ import annotations

from typing import Any, Mapping

from sqlalchemy_mutable import Mutable, MutableDict, MutableList as MutableListBase
from sqlalchemy_mutable.types import MutableJSONType, MutablePickleType
from sqlalchemy_mutable.utils import is_instance


class MutableList(MutableListBase):
    def convert_object(self, obj, root):
        if obj is None:
            obj = []
        if not is_instance(obj, list):
            obj = [obj]
        return super().convert_object(obj, root)


class MutableListJSONType(MutableJSONType):
    pass


MutableList.associate_with(MutableListJSONType)


class MutableListPickleType(MutablePickleType):
    pass


MutableList.associate_with(MutableListPickleType)


class MutableChoiceList(MutableList):
    cache_ok = False

    def _convert_item(self, item: Any, root: Mutable = None) -> MutableDict:
        """Convert a choice item to a dictionary.

        The converted item is an attributes dictionary with at least "value" and
        "label" keys. Items that are not mappings will be converted to a dictionary.
        If the item is a tuple, the item is interpreted as a (value, label) tuple.
        Otherwise, the item is interpreted as both the value and label.

        Args:
            item (Any): Choice.
            root (Mutable, optional): Root mutable object. Defaults to None.

        Returns:
            MutableDict: Converted choice object.
        """
        if is_instance(item, Mapping):
            item = dict(item)
            item.setdefault("value", None)
            item.setdefault("label", item["value"])
            return super()._convert_item(item, root)

        if item is None:
            value = label = None
        elif is_instance(item, tuple):
            value, label = item
        else:
            value = label = item
        return super()._convert_item({"value": value, "label": label}, root)


class MutableChoiceListType(MutableJSONType):
    pass


MutableChoiceList.associate_with(MutableChoiceListType)
