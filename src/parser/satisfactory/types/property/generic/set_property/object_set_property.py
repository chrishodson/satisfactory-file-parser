from parser.satisfactory.types.structs.object_reference import ObjectReference
from parser.satisfactory.types.property.generic.object_property import ObjectProperty
from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty

class ObjectSetProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, values: list[ObjectReference], ue_type: str = 'ObjectSetProperty', index: int = 0):
        super().__init__('ObjectSetProperty', ue_type, '', None, index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader, element_count: int, subtype: str, ue_type: str, index: int = 0):
        values = [ObjectProperty.read_value(reader) for _ in range(element_count)]
        return ObjectSetProperty(subtype, values, ue_type, index)

    @staticmethod
    def serialize(writer, property):
        for value in property.values:
            ObjectProperty.serialize_value(writer, value)
