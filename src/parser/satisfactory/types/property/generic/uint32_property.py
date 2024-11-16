from src.parser.byte.binary_readable import BinaryReadable
from src.parser.byte.byte_writer import ByteWriter
from src.parser.satisfactory.types.structs.guid_info import GUIDInfo
from src.parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty

def is_uint32_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'UInt32Property'

class Uint32Property(AbstractBaseProperty):

    def __init__(self, value: int, ue_type: str = 'UInt32Property', guid_info: GUIDInfo = None, index: int = 0):
        super().__init__(type='UInt32Property', ue_type=ue_type, guid_info=guid_info, index=index)
        self.value = value

    @staticmethod
    def parse(reader: BinaryReadable, ue_type: str, index: int = 0) -> 'Uint32Property':
        guid_info = GUIDInfo.read(reader)
        value = Uint32Property.read_value(reader)
        return Uint32Property(value, ue_type, guid_info, index)

    @staticmethod
    def read_value(reader: BinaryReadable) -> int:
        return reader.read_uint32()

    @staticmethod
    def calc_overhead(property: 'Uint32Property') -> int:
        return 1

    @staticmethod
    def serialize(writer: ByteWriter, property: 'Uint32Property') -> None:
        GUIDInfo.write(writer, property.guid_info)
        Uint32Property.serialize_value(writer, property.value)

    @staticmethod
    def serialize_value(writer: ByteWriter, value: int) -> None:
        writer.write_uint32(value)
