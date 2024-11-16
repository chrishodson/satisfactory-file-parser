from ....byte.binary_readable import BinaryReadable
from ....byte.byte_writer import ByteWriter
from ..abstract_base_property import AbstractBaseProperty
from ..enum_property import EnumProperty

def is_enum_array_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'EnumArrayProperty'

class EnumArrayProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, values: list[str], ue_type: str = 'EnumArrayProperty', index: int = 0):
        super().__init__('EnumArrayProperty', ue_type, '', None, index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader: BinaryReadable, element_count: int, subtype: str, ue_type: str, index: int = 0) -> 'EnumArrayProperty':
        values = [EnumProperty.read_value(reader) for _ in range(element_count)]
        return EnumArrayProperty(subtype, values, ue_type, index)

    @staticmethod
    def serialize(writer: ByteWriter, property: 'EnumArrayProperty') -> None:
        for value in property.values:
            EnumProperty.serialize_value(writer, value)
