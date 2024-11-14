from ....byte.binary_readable import BinaryReadable
from ....byte.byte_writer import ByteWriter
from ...structs.guid_info import GUIDInfo
from .abstract_base_property import AbstractBaseProperty


def is_double_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'DoubleProperty'


class DoubleProperty(AbstractBaseProperty):

    def __init__(self, value: float, ue_type: str = 'DoubleProperty', guid_info: GUIDInfo = None, index: int = 0):
        super().__init__(type='DoubleProperty', ue_type=ue_type, guid_info=guid_info, index=index)
        self.value = value

    @staticmethod
    def parse(reader: BinaryReadable, ue_type: str, index: int = 0) -> 'DoubleProperty':
        guid_info = GUIDInfo.read(reader)
        value = DoubleProperty.read_value(reader)
        return DoubleProperty(value, ue_type, guid_info, index)

    @staticmethod
    def read_value(reader: BinaryReadable) -> float:
        return reader.read_double()

    @staticmethod
    def calc_overhead(property: 'DoubleProperty') -> int:
        return 1

    @staticmethod
    def serialize(writer: ByteWriter, property: 'DoubleProperty') -> None:
        GUIDInfo.write(writer, property.guid_info)
        DoubleProperty.serialize_value(writer, property.value)

    @staticmethod
    def serialize_value(writer: ByteWriter, value: float) -> None:
        writer.write_double(value)
