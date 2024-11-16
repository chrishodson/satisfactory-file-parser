from parser.satisfactory.types.structs.guid_info import GUIDInfo
from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty

def is_str_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'StrProperty'

class StrProperty(AbstractBaseProperty):

    def __init__(self, value: str, ue_type: str = 'StrProperty', guid_info: GUIDInfo = None, index: int = 0):
        super().__init__('StrProperty', ue_type, '', guid_info, index)
        self.value = value

    @staticmethod
    def parse(reader: 'BinaryReadable', ue_type: str, index: int = 0) -> 'StrProperty':
        guid_info = GUIDInfo.read(reader)
        value = StrProperty.read_value(reader)
        return StrProperty(value, ue_type, guid_info, index)

    @staticmethod
    def read_value(reader: 'BinaryReadable') -> str:
        return reader.read_string()

    @staticmethod
    def calc_overhead(property: 'StrProperty') -> int:
        return 1

    @staticmethod
    def serialize(writer: 'ByteWriter', property: 'StrProperty') -> None:
        GUIDInfo.write(writer, property.guid_info)
        StrProperty.serialize_value(writer, property.value)

    @staticmethod
    def serialize_value(writer: 'ByteWriter', value: str) -> None:
        writer.write_string(value)
