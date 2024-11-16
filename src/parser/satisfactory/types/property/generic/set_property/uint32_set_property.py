from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty
from parser.satisfactory.types.property.generic.uint32_property import Uint32Property

class Uint32SetProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, ue_type: str, index: int = 0):
        super().__init__('Uint32SetProperty', ue_type, index=index)
        self.subtype = subtype
        self.values = []

    @staticmethod
    def parse(reader, element_count: int, subtype: str, ue_type: str, index: int = 0):
        values = [Uint32Property.read_value(reader) for _ in range(element_count)]
        property = Uint32SetProperty(subtype, ue_type, index)
        property.values = values
        return property

    @staticmethod
    def serialize(writer, property):
        for value in property.values:
            Uint32Property.serialize_value(writer, value)
