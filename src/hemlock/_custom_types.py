from sqlalchemy_mutable import MutableList as MutableListBase
from sqlalchemy_mutable.types import MutableJSONType, MutablePickleType
from sqlalchemy_mutable.utils import is_instance


class MutableList(MutableListBase):
    @staticmethod
    def convert_object(obj, root):
        if obj is None:
            return []
        if not is_instance(obj, list):
            return [obj]
        return MutableListBase.convert_object(obj, root)


class MutableListJSONType(MutableJSONType):
    pass


MutableList.associate_with(MutableListJSONType)


class MutableListPickleType(MutablePickleType):
    pass


MutableList.associate_with(MutableListPickleType)
