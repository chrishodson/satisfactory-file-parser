from parser.satisfactory.types.structs.guid_info import GUIDInfo
from .abstract_base_property import AbstractBaseProperty

class FloatProperty(AbstractBaseProperty):

    def __init__(self, value: float, ue_type: str = 'FloatProperty', guid_info: GUIDInfo = None, index: int = 0):
        super().__init__('FloatProperty', ue_type, '', guid_info, index)
        self.value = value

    @staticmethod
    def parse(reader, ue_type: str, index: int = 0):
        guid_info = GUIDInfo.read(reader)
        value = FloatProperty.read_value(reader)
        return FloatProperty(value, ue_type, guid_info, index)

    @staticmethod
    def calc_overhead(property):
        return 1

    @staticmethod
    def read_value(reader):
        return reader.read_float32()

    @staticmethod
    def serialize(writer, property):
        GUIDInfo.write(writer, property.guid_info)
        FloatProperty.serialize_value(writer, property.value)

    @staticmethod
    def serialize_value(writer, value):
        writer.write_float32(value)
