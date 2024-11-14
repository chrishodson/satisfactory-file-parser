from ....byte.binary_readable import BinaryReadable
from ....byte.byte_writer import ByteWriter
from ...structs.GUIDInfo import GUIDInfo
from .abstract_base_property import AbstractBaseProperty

def is_enum_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'EnumProperty'

class EnumProperty(AbstractBaseProperty):

    def __init__(self, value: dict, ue_type: str = 'EnumProperty', guid_info: GUIDInfo = None, index: int = 0):
        super().__init__({'type': 'EnumProperty', 'ueType': ue_type, 'guidInfo': guid_info, 'index': index})
        self.value = value

    @staticmethod
    def parse(reader: BinaryReadable, ue_type: str, index: int = 0) -> 'EnumProperty':
        name = reader.read_string()
        guid_info = GUIDInfo.read(reader)
        value = EnumProperty.read_value(reader)
        return EnumProperty({'name': name, 'value': value}, ue_type, guid_info, index)

    @staticmethod
    def read_value(reader: BinaryReadable) -> str:
        return reader.read_string()

    @staticmethod
    def calc_overhead(property: 'EnumProperty') -> int:
        return len(property.value['name']) + 5 + 1

    @staticmethod
    def serialize(writer: ByteWriter, property: 'EnumProperty') -> None:
        writer.write_string(property.value['name'])
        GUIDInfo.write(writer, property.guid_info)
        EnumProperty.serialize_value(writer, property.value['value'])

    @staticmethod
    def serialize_value(writer: ByteWriter, value: str) -> None:
        writer.write_string(value)
