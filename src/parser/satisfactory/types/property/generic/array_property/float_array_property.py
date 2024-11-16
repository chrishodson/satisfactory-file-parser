from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty
from parser.satisfactory.types.property.generic.float_property import FloatProperty

def is_float_array_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'FloatArrayProperty'

class FloatArrayProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, values: list[float], ue_type: str = 'FloatArrayProperty', index: int = 0):
        super().__init__('FloatArrayProperty', ue_type, '', None, index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader: BinaryReadable, element_count: int, subtype: str, ue_type: str, index: int = 0) -> 'FloatArrayProperty':
        values = [FloatProperty.read_value(reader) for _ in range(element_count)]
        return FloatArrayProperty(subtype, values, ue_type, index)

    @staticmethod
    def serialize(writer: ByteWriter, property: 'FloatArrayProperty') -> None:
        for value in property.values:
            FloatProperty.serialize_value(writer, value)
