from parser.satisfactory.types.structs.guid_info import GUIDInfo
from parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty


class Uint64Property(AbstractBaseProperty):

    def __init__(self, value: str, ue_type: str = 'UInt64Property', guid_info: GUIDInfo = None, index: int = 0):
        super().__init__('UInt64Property', ue_type, '', guid_info, index)
        self.value = value

    @staticmethod
    def parse(reader, ue_type: str, index: int = 0):
        guid_info = GUIDInfo.read(reader)
        value = Uint64Property.read_value(reader)
        return Uint64Property(value, ue_type, guid_info, index)

    @staticmethod
    def read_value(reader):
        return str(reader.read_uint64())

    @staticmethod
    def calc_overhead(property):
        return 1

    @staticmethod
    def serialize(writer, property):
        GUIDInfo.write(writer, property.guid_info)
        Uint64Property.serialize_value(writer, property.value)

    @staticmethod
    def serialize_value(writer, value: str):
        writer.write_uint64(int(value))
