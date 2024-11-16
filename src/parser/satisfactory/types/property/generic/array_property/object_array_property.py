from parser.satisfactory.types.structs.object_reference import ObjectReference
from parser.satisfactory.types.property.generic.object_property import ObjectProperty
from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty

class ObjectArrayProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, ue_type: str, values: list[ObjectReference], index: int = 0):
        super().__init__('ObjectArrayProperty', ue_type, '', None, index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader, element_count: int, subtype: str, ue_type: str, index: int = 0):
        values = [ObjectProperty.read_value(reader) for _ in range(element_count)]
        return ObjectArrayProperty(subtype, ue_type, values, index)

    @staticmethod
    def serialize(writer, property):
        for value in property.values:
            ObjectProperty.serialize_value(writer, value)
