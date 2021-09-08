from sqlalchemy_mutable import MutableList as MutableListBase
from sqlalchemy_mutable.types import MutableJSONType, MutablePickleType


class MutableList(MutableListBase):
    @staticmethod
    def convert_object(obj, root):
        if obj is None:
            return []
        if not isinstance(obj, list):
            return [obj]
        return super().convert_object(obj, root)


class MutableListJSONType(MutableJSONType):
    pass


MutableList.associate_with(MutableListJSONType)


class MutableListPickleType(MutablePickleType):
    pass


MutableList.associate_with(MutableListPickleType)
