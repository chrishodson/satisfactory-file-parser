from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty
from parser.satisfactory.types.property.generic.bool_property import BoolProperty

class BoolArrayProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, ue_type: str, values: list[bool], index: int = 0):
        super().__init__('BoolArrayProperty', ue_type, '', None, index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader, element_count: int, subtype: str, ue_type: str, index: int = 0):
        values = [BoolProperty.read_value(reader) for _ in range(element_count)]
        return BoolArrayProperty(subtype, ue_type, values, index)

    @staticmethod
    def serialize(writer, property):
        for value in property.values:
            BoolProperty.serialize_value(writer, value)
