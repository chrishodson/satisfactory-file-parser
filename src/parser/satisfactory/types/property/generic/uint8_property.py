from parser.satisfactory.types.structs.guid_info import GUIDInfo
from .abstract_base_property import AbstractBaseProperty

def is_uint8_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'UInt8Property'

class Uint8Property(AbstractBaseProperty):

    def __init__(self, value: int, ue_type: str = 'UInt8Property', guid_info: GUIDInfo = None, index: int = 0):
        super().__init__('UInt8Property', ue_type, '', guid_info, index)
        self.value = value

    @staticmethod
    def parse(reader: BinaryReadable, ue_type: str, index: int = 0) -> 'Uint8Property':
        guid_info = GUIDInfo.read(reader)
        value = Uint8Property.read_value(reader)
        return Uint8Property(value, ue_type, guid_info, index)

    @staticmethod
    def read_value(reader: BinaryReadable) -> int:
        return reader.read_uint8()

    @staticmethod
    def calc_overhead(property: 'Uint8Property') -> int:
        return 1

    @staticmethod
    def serialize(writer: ByteWriter, property: 'Uint8Property') -> None:
        GUIDInfo.write(writer, property.guid_info)
        Uint8Property.serialize_value(writer, property.value)

    @staticmethod
    def serialize_value(writer: ByteWriter, value: int) -> None:
        writer.write_uint8(value)
