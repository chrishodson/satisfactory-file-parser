from ......byte.binary_readable import BinaryReadable
from ......byte.byte_writer import ByteWriter
from ..abstract_base_property import AbstractBaseProperty
from ..byte_property import ByteProperty

def is_byte_array_property(property):
    return not isinstance(property, list) and property.type == 'ByteArrayProperty'

class ByteArrayProperty(AbstractBaseProperty):
    def __init__(self, values, subtype, ue_type, index=0):
        super().__init__(type='ByteArrayProperty', ue_type=ue_type, index=index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader: BinaryReadable, element_count: int, subtype: str, ue_type: str, index: int = 0):
        values = [ByteProperty.read_value(reader) for _ in range(element_count)]
        return ByteArrayProperty(values, subtype, ue_type, index)

    @staticmethod
    def serialize(writer: ByteWriter, property):
        for value in property.values:
            ByteProperty.serialize_value(writer, value)
