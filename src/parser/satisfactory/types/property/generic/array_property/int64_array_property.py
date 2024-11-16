from src.parser.byte.binary_readable import BinaryReadable
from src.parser.byte.byte_writer import ByteWriter
from src.parser.satisfactory.types.property.generic.abstract_base_property import AbstractBaseProperty
from src.parser.satisfactory.types.property.generic.int64_property import Int64Property

def is_int64_array_property(property: any) -> bool:
    return not isinstance(property, list) and property.type == 'Int64ArrayProperty'

class Int64ArrayProperty(AbstractBaseProperty):
    def __init__(self, subtype: str, values: list[str], ue_type: str = 'Int64ArrayProperty', index: int = 0):
        super().__init__(type='Int64ArrayProperty', ue_type=ue_type, index=index)
        self.subtype = subtype
        self.values = values

    @staticmethod
    def parse(reader: BinaryReadable, element_count: int, subtype: str, ue_type: str, index: int = 0) -> 'Int64ArrayProperty':
        values = [Int64Property.read_value(reader) for _ in range(element_count)]
        return Int64ArrayProperty(subtype, values, ue_type, index)

    @staticmethod
    def serialize(writer: ByteWriter, property: 'Int64ArrayProperty') -> None:
        for value in property.values:
            Int64Property.serialize_value(writer, value)
