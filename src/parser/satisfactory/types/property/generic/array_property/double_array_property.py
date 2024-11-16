from ....byte.binary_readable import BinaryReadable
from ....byte.byte_writer import ByteWriter
from ..abstract_base_property import AbstractBaseProperty
from ..double_property import DoubleProperty

def is_double_array_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'DoubleArrayProperty'

class DoubleArrayProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, values: list[float], ue_type: str = 'DoubleArrayProperty', index: int = 0):
        super().__init__(type='DoubleArrayProperty', ue_type=ue_type, index=index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader: BinaryReadable, element_count: int, subtype: str, ue_type: str, index: int = 0) -> 'DoubleArrayProperty':
        values = [DoubleProperty.read_value(reader) for _ in range(element_count)]
        return DoubleArrayProperty(subtype, values, ue_type, index)

    @staticmethod
    def serialize(writer: ByteWriter, property: 'DoubleArrayProperty') -> None:
        for value in property.values:
            DoubleProperty.serialize_value(writer, value)
