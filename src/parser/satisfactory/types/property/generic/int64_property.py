from src.parser.byte.binary_readable import BinaryReadable
from src.parser.byte.byte_writer import ByteWriter
from src.parser.satisfactory.types.structs.guid_info import GUIDInfo
from src.parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty

def is_int64_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'Int64Property'

class Int64Property(AbstractBaseProperty):

    def __init__(self, value: str, ue_type: str = 'Int64Property', guid_info: GUIDInfo = None, index: int = 0):
        super().__init__(type='Int64Property', ue_type=ue_type, guid_info=guid_info, index=index)
        self.value = value

    @staticmethod
    def parse(reader: BinaryReadable, ue_type: str, index: int = 0) -> 'Int64Property':
        guid_info = GUIDInfo.read(reader)
        value = Int64Property.read_value(reader)
        return Int64Property(value, ue_type, guid_info, index)

    @staticmethod
    def read_value(reader: BinaryReadable) -> str:
        return str(reader.read_int64())

    @staticmethod
    def calc_overhead(property: 'Int64Property') -> int:
        return 1

    @staticmethod
    def serialize(writer: ByteWriter, property: 'Int64Property') -> None:
        GUIDInfo.write(writer, property.guid_info)
        Int64Property.serialize_value(writer, property.value)

    @staticmethod
    def serialize_value(writer: ByteWriter, value: str) -> None:
        writer.write_int64(int(value))
