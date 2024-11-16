from parser.satisfactory.types.structs.guid_info import GUIDInfo
from .abstract_base_property import AbstractBaseProperty

def is_int8_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'Int8Property'

class Int8Property(AbstractBaseProperty):

    def __init__(self, value: int, ue_type: str = 'Int8Property', guid_info: GUIDInfo = None, index: int = 0):
        super().__init__('Int8Property', ue_type, guid_info, index)
        self.value = value

    @staticmethod
    def parse(reader: 'BinaryReadable', ue_type: str, index: int = 0) -> 'Int8Property':
        guid_info = GUIDInfo.read(reader)
        value = Int8Property.read_value(reader)
        return Int8Property(value, ue_type, guid_info, index)

    @staticmethod
    def read_value(reader: 'BinaryReadable') -> int:
        return reader.read_int8()

    @staticmethod
    def calc_overhead(property: 'Int8Property') -> int:
        return 1

    @staticmethod
    def serialize(writer: 'ByteWriter', property: 'Int8Property') -> None:
        GUIDInfo.write(writer, property.guid_info)
        Int8Property.serialize_value(writer, property.value)

    @staticmethod
    def serialize_value(writer: 'ByteWriter', value: int) -> None:
        writer.write_int8(value)
