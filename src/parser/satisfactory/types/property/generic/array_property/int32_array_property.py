from src.parser.byte.binary_readable import BinaryReadable
from src.parser.byte.byte_writer import ByteWriter
from src.parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty
from src.parser.satisfactory.types.property.generic.int32_property import Int32Property

def is_int32_array_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'Int32ArrayProperty'

class Int32ArrayProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, values: list[int], ue_type: str = 'Int32ArrayProperty', index: int = 0):
        super().__init__(type='Int32ArrayProperty', ue_type=ue_type, index=index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader: BinaryReadable, element_count: int, subtype: str, ue_type: str, index: int = 0) -> 'Int32ArrayProperty':
        values = [Int32Property.read_value(reader) for _ in range(element_count)]
        return Int32ArrayProperty(subtype, values, ue_type, index)

    @staticmethod
    def serialize(writer: ByteWriter, property: 'Int32ArrayProperty') -> None:
        for value in property.values:
            Int32Property.serialize_value(writer, value)
