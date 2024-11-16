from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty
from parser.satisfactory.types.property.generic.str_property import StrProperty

def is_str_array_property(property):
    return not isinstance(property, list) and property.type == 'StrArrayProperty'

class StrArrayProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, values: list[str], ue_type: str, index: int = 0):
        super().__init__('StrArrayProperty', ue_type, '', None, index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader, element_count: int, subtype: str, ue_type: str, index: int = 0):
        values = [StrProperty.read_value(reader) for _ in range(element_count)]
        return StrArrayProperty(subtype, values, ue_type, index)

    @staticmethod
    def serialize(writer, property):
        for value in property.values:
            StrProperty.serialize_value(writer, value)
