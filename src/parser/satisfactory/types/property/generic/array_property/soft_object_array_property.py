from parser.satisfactory.types.structs.soft_object_reference import SoftObjectReference
from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty
from parser.satisfactory.types.property.generic.soft_object_property import SoftObjectProperty

class SoftObjectArrayProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, values: list[SoftObjectReference], ue_type: str, index: int = 0):
        super().__init__('SoftObjectArrayProperty', ue_type, '', None, index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader, element_count: int, subtype: str, ue_type: str, index: int = 0):
        values = [SoftObjectProperty.read_value(reader) for _ in range(element_count)]
        return SoftObjectArrayProperty(subtype, values, ue_type, index)

    @staticmethod
    def serialize(writer, property):
        for value in property.values:
            SoftObjectProperty.serialize_value(writer, value)
